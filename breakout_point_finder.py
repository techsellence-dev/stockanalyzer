import os
import pandas as pd
import datetime
import numpy as np

from constants.break_even_calculation_constants import ALL_TIME_MAX, ALL_TIME_MAX_DATE, LAST_ONE_YEAR_MAX, \
    LAST_TWO_YEARS_MAX, LAST_TWO_YEARS_MAX_DATE, LAST_THREE_YEARS_MAX_DATE, LAST_THREE_YEARS_MAX, LAST_FOUR_YEARS_MAX, \
    LAST_FOUR_YEARS_MAX_DATE, LAST_FIVE_YEARS_MAX, LAST_FIVE_YEARS_MAX_DATE, LAST_ONE_YEAR_MAX_DATE, CURRENT_PRICE


def get_past_max(historical_stock_df, grouped_by_year_historical_df, n):
    current_year = datetime.date.today().year
    past_n_years_df = grouped_by_year_historical_df[grouped_by_year_historical_df.Date >= current_year - n]
    past_n_years_max_df = past_n_years_df[past_n_years_df.Close == past_n_years_df.Close.max()].reset_index(drop=True)
    past_n_years_max_value = past_n_years_max_df.iloc[0]['Close']
    past_n_years_max_date_df = historical_stock_df.loc[(historical_stock_df['Date'].dt.year >= current_year - n) &
                                                       (
                                                                   historical_stock_df.Close == past_n_years_max_value)].reset_index(
        drop=True)
    past_n_years_max_date = past_n_years_max_date_df.iloc[0]['Complete Date']
    return past_n_years_max_value, past_n_years_max_date


def get_all_time_max(historical_stock_df, grouped_by_year_historical_df):
    all_time_max_df = grouped_by_year_historical_df[
        grouped_by_year_historical_df.Close == grouped_by_year_historical_df.Close.max()].reset_index(drop=True)
    max_value = all_time_max_df.iloc[0]['Close']
    max_df = historical_stock_df.loc[historical_stock_df.Close == max_value].reset_index(drop=True)
    max_date = max_df.iloc[0]['Complete Date']
    return max_value, max_date


def find_breakout_point(stock_symbol):
    past_max_dict = {}
    output_dir = os.getcwd() + '/StockData/Output/' + stock_symbol
    output_data_path = output_dir + '/historical_data'
    historical_stock_df = pd.read_csv(output_data_path)
    try:
        historical_stock_df['Complete Date'] = historical_stock_df['Date']
        historical_stock_df['Date'] = pd.to_datetime(historical_stock_df['Date'], errors='coerce').to_frame()
        grouped_by_year_historical_df = historical_stock_df.groupby(historical_stock_df.Date.dt.year)[
            'Close'].max().reset_index()

        # Current Price
        current_price = historical_stock_df.iloc[-1]['Close']
        past_max_dict[CURRENT_PRICE] = current_price
        # All Time Max
        all_time_max_value, all_time_max_date = get_all_time_max(historical_stock_df, grouped_by_year_historical_df)
        past_max_dict[ALL_TIME_MAX] = all_time_max_value
        past_max_dict[ALL_TIME_MAX_DATE] = all_time_max_date
        # Past one year max
        one_year_max_value, one_year_max_date = get_past_max(historical_stock_df, grouped_by_year_historical_df, 1)
        past_max_dict[LAST_ONE_YEAR_MAX] = one_year_max_value
        past_max_dict[LAST_ONE_YEAR_MAX_DATE] = one_year_max_date
        # Past two years max
        two_year_max_value, two_year_max_date = get_past_max(historical_stock_df, grouped_by_year_historical_df, 2)
        past_max_dict[LAST_TWO_YEARS_MAX] = two_year_max_value
        past_max_dict[LAST_TWO_YEARS_MAX_DATE] = two_year_max_date
        # Past three years max
        three_year_max_value, three_year_max_date = get_past_max(historical_stock_df, grouped_by_year_historical_df, 3)
        past_max_dict[LAST_THREE_YEARS_MAX] = three_year_max_value
        past_max_dict[LAST_THREE_YEARS_MAX_DATE] = three_year_max_date
        # Past four years max
        four_year_max_value, four_year_max_date = get_past_max(historical_stock_df, grouped_by_year_historical_df, 4)
        past_max_dict[LAST_FOUR_YEARS_MAX] = four_year_max_value
        past_max_dict[LAST_FOUR_YEARS_MAX_DATE] = four_year_max_date
        # Past five years max
        five_year_max_value, five_year_max_date = get_past_max(historical_stock_df, grouped_by_year_historical_df, 5)
        past_max_dict[LAST_FIVE_YEARS_MAX] = five_year_max_value
        past_max_dict[LAST_FIVE_YEARS_MAX_DATE] = five_year_max_date

        print('Stock Symbol: ' + stock_symbol + ', past max data: ' + str(past_max_dict))
        return past_max_dict
    except Exception as e:
        print('Breakout point calculation failed for stock: ' + stock_symbol + ', due to: ' + str(e))
        raise e
