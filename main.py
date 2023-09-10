# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import os

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

import breakout_point_finder
import ticker_info_updater

from constants.break_even_calculation_constants import ALL_TIME_MAX, ALL_TIME_MAX_DATE, LAST_ONE_YEAR_MAX, \
    LAST_TWO_YEARS_MAX, LAST_TWO_YEARS_MAX_DATE, LAST_THREE_YEARS_MAX_DATE, LAST_THREE_YEARS_MAX, LAST_FOUR_YEARS_MAX, \
    LAST_FOUR_YEARS_MAX_DATE, LAST_FIVE_YEARS_MAX, LAST_FIVE_YEARS_MAX_DATE, LAST_ONE_YEAR_MAX_DATE, CURRENT_PRICE, \
    ALL_TIME_MIN, ALL_TIME_MIN_DATE, PRICE_DIFF_ATH, DISTANCE_FROM_ATH, PRICE_DIFF_ATL, DISTANCE_FROM_ATL, \
    PRICE_DIFF_1YH, DISTANCE_FROM_1YH, PRICE_DIFF_2YH, DISTANCE_FROM_2YH, PRICE_DIFF_3YH, DISTANCE_FROM_3YH, \
    PRICE_DIFF_4YH, DISTANCE_FROM_4YH, PRICE_DIFF_5YH, DISTANCE_FROM_5YH, LAST_ONE_YEAR_MIN, LAST_ONE_YEAR_MIN_DATE, \
    PRICE_DIFF_1YL, DISTANCE_FROM_1YL, LAST_TWO_YEARS_MIN, LAST_TWO_YEARS_MIN_DATE, PRICE_DIFF_2YL, DISTANCE_FROM_2YL, \
    LAST_THREE_YEARS_MIN, LAST_THREE_YEARS_MIN_DATE, PRICE_DIFF_3YL, DISTANCE_FROM_3YL, LAST_FOUR_YEARS_MIN, \
    LAST_FOUR_YEARS_MIN_DATE, PRICE_DIFF_4YL, DISTANCE_FROM_4YL, LAST_FIVE_YEARS_MIN, LAST_FIVE_YEARS_MIN_DATE, \
    PRICE_DIFF_5YL, DISTANCE_FROM_5YL


def download_and_save_individual_stock_data(stock_symbol):
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
    nse_stock_symbols['Industry'] = 'N/A'
    nse_stock_symbols['Source'] = 'NSE'
    bse_stock_symbols = pd.DataFrame(bse_stocks, columns=['Issuer Name', 'ISIN No'])
    bse_stock_symbols['Source'] = 'BSE'
    nse_stock_symbols.rename(columns={'Symbol': 'Stock Symbol'}, inplace=True)
    bse_stock_symbols.rename(columns={'Issuer Name': 'Stock Symbol'}, inplace=True)
    bse_stock_symbols.rename(columns={'ISIN No': 'Industry'}, inplace=True)
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
            download_and_save_individual_stock_data(stock_symbol)
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


def find_and_save_breakout_points(week_list_for_past_stats, week_list_for_price_movement, days_list_for_moving_average):
    row_list = []
    global stock_symbol
    stocks_df = pd.read_csv(os.getcwd() + '/StockData/Output/DedupedStockSymbols')
    for ind in stocks_df.index:
        if stocks_df['Source'][ind] == 'NSE':
            stock_symbol = str(stocks_df['Stock Symbol'][ind]) + '.NS'
        elif stocks_df['Source'][ind] == 'BSE':
            stock_symbol = str(stocks_df['Stock Symbol'][ind]) + '.BO'
        try:
            industry = stocks_df['Industry'][ind]
            breakout_details_dict = {'Stock Symbol': stock_symbol, 'Industry': industry}
            breakout_details_dict.update(ticker_info_updater.update_ticker_info(stock_symbol))
            breakout_details_dict.update(breakout_point_finder.find_breakout_point(stock_symbol,
                        week_list_for_past_stats, week_list_for_price_movement, days_list_for_moving_average))
            row_list.append(breakout_details_dict)
        except Exception as e:
            print('Could not derive past max prices for symbol: ' + stock_symbol + ' due to data unavailability, '
                                                                                   'exception: ' + str(e))
    output_df = pd.DataFrame(row_list)
    output_df_with_past_at_data = output_df[
        ['Stock Symbol', 'Industry', 'Current Price', ALL_TIME_MAX, ALL_TIME_MAX_DATE, PRICE_DIFF_ATH,
         DISTANCE_FROM_ATH,
         ALL_TIME_MIN, ALL_TIME_MIN_DATE, PRICE_DIFF_ATL, DISTANCE_FROM_ATL]]

    output_df_with_past_1Y_data = output_df[
        ['Stock Symbol', 'Industry', 'Current Price',
         LAST_ONE_YEAR_MAX, LAST_ONE_YEAR_MAX_DATE, PRICE_DIFF_1YH, DISTANCE_FROM_1YH,
         LAST_ONE_YEAR_MIN, LAST_ONE_YEAR_MIN_DATE, PRICE_DIFF_1YL, DISTANCE_FROM_1YL]]

    output_df_with_past_2Y_data = output_df[
        ['Stock Symbol', 'Industry', 'Current Price',
         LAST_TWO_YEARS_MAX, LAST_TWO_YEARS_MAX_DATE, PRICE_DIFF_2YH, DISTANCE_FROM_2YH,
         LAST_TWO_YEARS_MIN, LAST_TWO_YEARS_MIN_DATE, PRICE_DIFF_2YL, DISTANCE_FROM_2YL]]

    output_df_with_past_3Y_data = output_df[
        ['Stock Symbol', 'Industry', 'Current Price',
         LAST_THREE_YEARS_MAX, LAST_THREE_YEARS_MAX_DATE, PRICE_DIFF_3YH, DISTANCE_FROM_3YH,
         LAST_THREE_YEARS_MIN, LAST_THREE_YEARS_MIN_DATE, PRICE_DIFF_3YL, DISTANCE_FROM_3YL]]

    output_df_with_past_4Y_data = output_df[
        ['Stock Symbol', 'Industry', 'Current Price',
         LAST_FOUR_YEARS_MAX, LAST_FOUR_YEARS_MAX_DATE, PRICE_DIFF_4YH, DISTANCE_FROM_4YH,
         LAST_FOUR_YEARS_MIN, LAST_FOUR_YEARS_MIN_DATE, PRICE_DIFF_4YL, DISTANCE_FROM_4YL]]

    output_df_with_past_5Y_data = output_df[
        ['Stock Symbol', 'Industry', 'Current Price',
         LAST_FIVE_YEARS_MAX, LAST_FIVE_YEARS_MAX_DATE, PRICE_DIFF_5YH, DISTANCE_FROM_5YH,
         LAST_FIVE_YEARS_MIN, LAST_FIVE_YEARS_MIN_DATE, PRICE_DIFF_5YL, DISTANCE_FROM_5YL
         ]]

    with pd.ExcelWriter(os.getcwd() + '/StockData/Output/1_BreakoutPointData.xlsx') as writer:
        output_df_with_past_at_data.to_excel(writer, sheet_name="All Time Stats", index=False)
        output_df_with_past_5Y_data.to_excel(writer, sheet_name="Past 5 Years Stats", index=False)
        output_df_with_past_4Y_data.to_excel(writer, sheet_name="Past 4 Years Stats", index=False)
        output_df_with_past_3Y_data.to_excel(writer, sheet_name="Past 3 Years Stats", index=False)
        output_df_with_past_2Y_data.to_excel(writer, sheet_name="Past 2 Years Stats", index=False)
        output_df_with_past_1Y_data.to_excel(writer, sheet_name="Past 1 Year Stats", index=False)

        for n in week_list_for_past_stats:
            LAST_N_WEEKS_MAX_VALUE = 'Last ' + str(n) + ' weeks max value'
            LAST_N_WEEKS_MAX_DATE = 'Last ' + str(n) + ' weeks max date'
            PRICE_DIFF_NWH = 'Price diff wrt last ' + str(n) + ' weeks high'
            DISTANCE_FROM_NWH = 'Distance in days from last ' + str(n) + ' weeks high'

            LAST_N_WEEKS_MIN_VALUE = 'Last ' + str(n) + ' weeks min value'
            LAST_N_WEEKS_MIN_DATE = 'Last ' + str(n) + ' weeks min date'
            PRICE_DIFF_NWL = 'Price diff wrt last ' + str(n) + ' weeks low'
            DISTANCE_FROM_NWL = 'Distance in days from last ' + str(n) + ' weeks low'

            output_df_with_past_n_weeks_data = output_df[['Stock Symbol', 'Industry', 'Current Price',
             LAST_N_WEEKS_MAX_VALUE, LAST_N_WEEKS_MAX_DATE, PRICE_DIFF_NWH, DISTANCE_FROM_NWH,
             LAST_N_WEEKS_MIN_VALUE, LAST_N_WEEKS_MIN_DATE, PRICE_DIFF_NWL, DISTANCE_FROM_NWL]]
            output_df_with_past_n_weeks_data.to_excel(writer, sheet_name="Past " + str(n) + " Weeks Stats", index=False)

        column_list_for_price_movement_data = ['Stock Symbol', 'Industry', 'Current Price']
        for n in week_list_for_price_movement:
            PRICE_N_WEEKS_BACK = 'Price ' + str(n) + ' weeks back'
            PRICE_MOVEMENT_IN_N_WEEKS = 'Price movement in ' + str(n) + ' weeks'

            column_list_for_price_movement_data.append(PRICE_N_WEEKS_BACK)
            column_list_for_price_movement_data.append(PRICE_MOVEMENT_IN_N_WEEKS)

        output_df_with_past_few_weeks_price_movement = output_df.filter(column_list_for_price_movement_data)
        output_df_with_past_few_weeks_price_movement.to_excel(writer, sheet_name="Past Few Weeks Price Movement", index=False)

        column_list_for_dma_data = ['Stock Symbol', 'Industry', 'Current Price']
        for n in days_list_for_moving_average:
            LAST_N_DAYS_PRICE_AVG = "Last " + str(n) + " days price average"
            PRICE_MOVEMENT_FROM_LAST_N_DAYS_AVERAGE = "Price movement from last " + str(n) + " days average"
            column_list_for_dma_data.append(LAST_N_DAYS_PRICE_AVG)
            column_list_for_dma_data.append(PRICE_MOVEMENT_FROM_LAST_N_DAYS_AVERAGE)
        output_df_with_dma_data = output_df.filter(column_list_for_dma_data)
        output_df_with_dma_data.to_excel(writer, sheet_name="Past Few Days Price Average",
                                                              index=False)
    print('Successfully wrote breakout point data for all listed NSE and BSE stocks to: '
          + os.getcwd() + '/StockData/Output/1_BreakoutPointData.xlsx')


if __name__ == '__main__':
    # deduplicate_stock_symbols()
    # download_historical_stock_data()
    # plot_and_save_historical_stock_data()
    find_and_save_breakout_points(week_list_for_past_stats = [26, 52],
                                  week_list_for_price_movement = [26, 99],
                                  days_list_for_moving_average = [200, 500])
