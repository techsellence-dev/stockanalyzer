# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import yfinance as yf
import os


def download_stock_data(stock_name):
    historical_data = yf.download(stock_name)
    output_dir = os.getcwd() + '/StockData/Output/' + stock_name
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    historical_data.to_csv(os.path.join(output_dir, 'historical_data'))
    print('Successfully downloaded stock data for symbol: ' + stock_name)

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
    deduped_stock_symbols = concatenated_stock_symbols.drop_duplicates(subset = ['Stock Symbol'], keep = 'first').reset_index(drop = True)
    print("Total number of stocks after concatenation and deduplication: " + str(deduped_stock_symbols.shape[0]))
    deduped_stock_symbols.to_csv(os.getcwd() + '/StockData/Output/DedupedStockSymbols')


def download_historical_stock_data():
    stocks_df = pd.read_csv(os.getcwd() + '/StockData/Output/DedupedStockSymbols')
    for ind in stocks_df.index:
        if stocks_df['Source'][ind] == 'NSE':
            download_stock_data(stocks_df['Stock Symbol'][ind] + '.NS')
        elif stocks_df['Source'][ind] == 'BSE':
            download_stock_data(stocks_df['Stock Symbol'][ind] + '.BO')


if __name__ == '__main__':
    deduplicate_stock_symbols()
    download_historical_stock_data()

