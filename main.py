# This is a sample Python script.
import json

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import yfinance as yf
import os
import matplotlib.pyplot as plt

import breakout_point_finder


def download_individual_stock_data(stock_symbol):
    historical_data = yf.download(stock_symbol)
    output_dir = os.getcwd() + '/StockData/Output/' + stock_symbol
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    historical_data.to_csv(os.path.join(output_dir, 'historical_data'))
    print('Successfully downloaded stock data for symbol: ' + stock_symbol)


def deduplicate_stock_symbols():
    nse_stocks = pd.read_csv(os.getcwd() + '/StockData/Input/NSE_Stocks.csv')
    num_nse_stocks, num_nse_stock_props = nse_stocks.shape
    print('Total number of NSE stocks: ' + str(num_nse_stocks))

    bse_stocks = pd.read_csv(os.getcwd() + '/StockData/Input/BSE_Stocks.csv')
    num_bse_stocks, num_bse_stock_props = bse_stocks.shape
    print('Total number of BSE stocks: ' + str(num_bse_stocks))

    nse_stock_symbols = nse_stocks['Symbol'].to_frame()
    nse_stock_symbols['Source'] = 'NSE'
    bse_stock_symbols = bse_stocks['Issuer Name'].to_frame()
    bse_stock_symbols['Source'] = 'BSE'
    nse_stock_symbols.rename(columns={'Symbol': 'Stock Symbol'}, inplace=True)
    bse_stock_symbols.rename(columns={'Issuer Name': 'Stock Symbol'}, inplace=True)
    concatenated_stock_symbols = pd.concat([nse_stock_symbols, bse_stock_symbols])
    deduped_stock_symbols = concatenated_stock_symbols.drop_duplicates(subset=['Stock Symbol'],
                                                                       keep='first').reset_index(drop=True)
    print("Total number of stocks after concatenation and deduplication: " + str(deduped_stock_symbols.shape[0]))
    deduped_stock_symbols.to_csv(os.getcwd() + '/StockData/Output/DedupedStockSymbols')


def download_historical_stock_data():
    global stock_symbol
    failed_download_dict = {}
    failed_download_file_path = os.getcwd() + '/StockData/Output/FailedDownload'
    if not os.path.exists(failed_download_file_path):
        os.mkdir(failed_download_file_path)
    stocks_df = pd.read_csv(os.getcwd() + '/StockData/Output/DedupedStockSymbols')
    for ind in stocks_df.index:
        if stocks_df['Source'][ind] == 'NSE':
            stock_symbol = str(stocks_df['Stock Symbol'][ind]) + '.NS'
        elif stocks_df['Source'][ind] == 'BSE':
            stock_symbol = str(stocks_df['Stock Symbol'][ind]) + '.BO'
        try:
            download_individual_stock_data(stock_symbol)
        except Exception as e:
            print('Could not download historical data for symbol: ' + stock_symbol + ', due to: ' + str(e))
            failed_download_dict[stock_symbol] = e
    print('Number of stocks for which download failed is: ' + str(len(failed_download_dict)))
    write_dict_to_file(failed_download_dict, failed_download_file_path + '/failed_items')


def plot_individual_stock(stock_symbol):
    output_dir = os.getcwd() + '/StockData/Output/' + stock_symbol
    output_data_path = output_dir + '/historical_data'
    output_plot_path = output_dir + '/' + stock_symbol + '.png'
    historical_stock_df = pd.read_csv(output_data_path)
    try:
        historical_stock_df.plot(x='Date', y=['Open', 'High', 'Low', 'Close'])
        plt.savefig(output_plot_path)
        print('Successfully saved historical stock data plot for stock: ' + stock_symbol)
    except Exception as e:
        print('Plotting Failed for stock: ' + stock_symbol + ', due to: ' + str(e))
        raise e


def plot_and_save_historical_stock_data():
    global stock_symbol
    failed_to_plot_dict = {}
    failed_plot_file_path = os.getcwd() + '/StockData/Output/FailedPlot'
    if not os.path.exists(failed_plot_file_path):
        os.mkdir(failed_plot_file_path)
    stocks_df = pd.read_csv(os.getcwd() + '/StockData/Output/DedupedStockSymbols')
    for ind in stocks_df.index:
        if stocks_df['Source'][ind] == 'NSE':
            stock_symbol = str(stocks_df['Stock Symbol'][ind]) + '.NS'
        elif stocks_df['Source'][ind] == 'BSE':
            stock_symbol = str(stocks_df['Stock Symbol'][ind]) + '.BO'
        try:
            plot_individual_stock(stock_symbol)
        except Exception as e:
            print('Could not plot symbol: ' + stock_symbol + ', due to: ' + str(e))
            failed_to_plot_dict[stock_symbol] = e
    print('Number of stocks failed to plot is: ' + str(len(failed_to_plot_dict)))
    write_dict_to_file(failed_to_plot_dict, failed_plot_file_path + '/failed_items')


def write_dict_to_file(kv_dict, file_name):
    with open(file_name, 'w') as output_file:
        output_file.write(str(kv_dict))


def find_and_save_breakout_points():
    row_list = []
    global stock_symbol
    stocks_df = pd.read_csv(os.getcwd() + '/StockData/Output/DedupedStockSymbols')
    for ind in stocks_df.index:
        if stocks_df['Source'][ind] == 'NSE':
            stock_symbol = str(stocks_df['Stock Symbol'][ind]) + '.NS'
        elif stocks_df['Source'][ind] == 'BSE':
            stock_symbol = str(stocks_df['Stock Symbol'][ind]) + '.BO'
        try:
            breakout_details_dict = {'Stock Symbol': stock_symbol}
            breakout_details_dict.update(breakout_point_finder.find_breakout_point(stock_symbol))
            row_list.append(breakout_details_dict)
        except Exception as e:
            print('Could not derive past max prices for symbol: ' + stock_symbol + ' due to data unavailability, '
                                                                                   'exception: ' + str(e))
    df_with_past_max_data = pd.DataFrame(row_list)
    df_with_past_max_data.to_csv(os.getcwd() + '/StockData/Output/BreakoutPointData.csv')
    print('Successfully wrote breakout point daa for all listed NSE and BSE stocks to: '
          + os.getcwd() + '/StockData/Output/BreakoutPointData.csv')


if __name__ == '__main__':
    deduplicate_stock_symbols()
    download_historical_stock_data()
    # plot_and_save_historical_stock_data()
    find_and_save_breakout_points()
