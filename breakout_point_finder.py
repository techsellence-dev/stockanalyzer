import datetime
import os

import pandas as pd

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


def get_past_max(historical_stock_df, grouped_by_year_historical_max_df, n):
    current_year = datetime.date.today().year
    past_n_years_df = grouped_by_year_historical_max_df[grouped_by_year_historical_max_df.Date >= current_year - n]
    past_n_years_max_df = past_n_years_df[past_n_years_df.Close == past_n_years_df.Close.max()].reset_index(drop=True)
    past_n_years_max_value = past_n_years_max_df.iloc[0]['Close']
    past_n_years_max_date_df = historical_stock_df.loc[(historical_stock_df['Date'].dt.year >= current_year - n) &
                                                       (
                                                               historical_stock_df.Close == past_n_years_max_value)].reset_index(
        drop=True)
    past_n_years_max_date = past_n_years_max_date_df.iloc[0]['Complete Date']
    return past_n_years_max_value, past_n_years_max_date


def get_past_min(historical_stock_df, grouped_by_year_historical_min_df, n):
    current_year = datetime.date.today().year
    past_n_years_df = grouped_by_year_historical_min_df[grouped_by_year_historical_min_df.Date >= current_year - n]
    past_n_years_min_df = past_n_years_df[past_n_years_df.Close == past_n_years_df.Close.min()].reset_index(drop=True)
    past_n_years_min_value = past_n_years_min_df.iloc[0]['Close']
    past_n_years_min_date_df = historical_stock_df.loc[(historical_stock_df['Date'].dt.year >= current_year - n) &
                                                       (
                                                               historical_stock_df.Close == past_n_years_min_value)].reset_index(
        drop=True)
    past_n_years_min_date = past_n_years_min_date_df.iloc[0]['Complete Date']
    return past_n_years_min_value, past_n_years_min_date


def get_all_time_max(historical_stock_df):
    max_value = historical_stock_df['Close'].max()
    max_df = historical_stock_df.loc[historical_stock_df.Close == max_value].reset_index(drop=True)
    max_date = max_df.iloc[0]['Complete Date']
    return max_value, max_date


def get_all_time_min(historical_stock_df):
    min_value = historical_stock_df['Close'].min()
    min_df = historical_stock_df.loc[historical_stock_df.Close == min_value].reset_index(drop=True)
    min_date = min_df.iloc[0]['Complete Date']
    return min_value, min_date


def find_difference_from_current_price(past_price, current_price):
    diff = round((current_price - past_price) / past_price * 100, 2)
    return str(diff) + '%'


def find_difference_from_current_date(all_time_max_date):
    return (datetime.datetime.now() - datetime.datetime.strptime(all_time_max_date, "%Y-%m-%d")).days


def find_breakout_point(stock_symbol):
    past_data_dict = {}
    output_dir = os.getcwd() + '/StockData/Output/' + stock_symbol
    output_data_path = output_dir + '/historical_data'
    historical_stock_df = pd.read_csv(output_data_path)
    try:
        historical_stock_df['Complete Date'] = historical_stock_df['Date']
        historical_stock_df['Date'] = pd.to_datetime(historical_stock_df['Date'], errors='coerce').to_frame()

        # Current Price
        current_price = historical_stock_df.iloc[-1]['Close']
        past_data_dict[CURRENT_PRICE] = current_price
        # All Time Max
        all_time_max_value, all_time_max_date = get_all_time_max(historical_stock_df)
        past_data_dict[ALL_TIME_MAX] = all_time_max_value
        past_data_dict[ALL_TIME_MAX_DATE] = all_time_max_date
        past_data_dict[PRICE_DIFF_ATH] = find_difference_from_current_price(all_time_max_value, current_price)
        past_data_dict[DISTANCE_FROM_ATH] = find_difference_from_current_date(all_time_max_date)
        # All Time Min
        all_time_min_value, all_time_min_date = get_all_time_min(historical_stock_df)
        past_data_dict[ALL_TIME_MIN] = all_time_min_value
        past_data_dict[ALL_TIME_MIN_DATE] = all_time_min_date
        past_data_dict[PRICE_DIFF_ATL] = find_difference_from_current_price(all_time_min_value, current_price)
        past_data_dict[DISTANCE_FROM_ATL] = find_difference_from_current_date(all_time_min_date)

        grouped_by_year_historical_max_df = historical_stock_df.groupby(historical_stock_df.Date.dt.year)[
            'Close'].max().reset_index()

        # Past one year max
        one_year_max_value, one_year_max_date = get_past_max(historical_stock_df, grouped_by_year_historical_max_df, 1)
        past_data_dict[LAST_ONE_YEAR_MAX] = one_year_max_value
        past_data_dict[LAST_ONE_YEAR_MAX_DATE] = one_year_max_date
        past_data_dict[PRICE_DIFF_1YH] = find_difference_from_current_price(one_year_max_value, current_price)
        past_data_dict[DISTANCE_FROM_1YH] = find_difference_from_current_date(one_year_max_date)
        # Past two years max
        two_year_max_value, two_year_max_date = get_past_max(historical_stock_df, grouped_by_year_historical_max_df, 2)
        past_data_dict[LAST_TWO_YEARS_MAX] = two_year_max_value
        past_data_dict[LAST_TWO_YEARS_MAX_DATE] = two_year_max_date
        past_data_dict[PRICE_DIFF_2YH] = find_difference_from_current_price(two_year_max_value, current_price)
        past_data_dict[DISTANCE_FROM_2YH] = find_difference_from_current_date(two_year_max_date)
        # Past three years max
        three_year_max_value, three_year_max_date = get_past_max(historical_stock_df, grouped_by_year_historical_max_df, 3)
        past_data_dict[LAST_THREE_YEARS_MAX] = three_year_max_value
        past_data_dict[LAST_THREE_YEARS_MAX_DATE] = three_year_max_date
        past_data_dict[PRICE_DIFF_3YH] = find_difference_from_current_price(three_year_max_value, current_price)
        past_data_dict[DISTANCE_FROM_3YH] = find_difference_from_current_date(three_year_max_date)
        # Past four years max
        four_year_max_value, four_year_max_date = get_past_max(historical_stock_df, grouped_by_year_historical_max_df, 4)
        past_data_dict[LAST_FOUR_YEARS_MAX] = four_year_max_value
        past_data_dict[LAST_FOUR_YEARS_MAX_DATE] = four_year_max_date
        past_data_dict[PRICE_DIFF_4YH] = find_difference_from_current_price(four_year_max_value, current_price)
        past_data_dict[DISTANCE_FROM_4YH] = find_difference_from_current_date(four_year_max_date)
        # Past five years max
        five_year_max_value, five_year_max_date = get_past_max(historical_stock_df, grouped_by_year_historical_max_df, 5)
        past_data_dict[LAST_FIVE_YEARS_MAX] = five_year_max_value
        past_data_dict[LAST_FIVE_YEARS_MAX_DATE] = five_year_max_date
        past_data_dict[PRICE_DIFF_5YH] = find_difference_from_current_price(five_year_max_value, current_price)
        past_data_dict[DISTANCE_FROM_5YH] = find_difference_from_current_date(five_year_max_date)

        grouped_by_year_historical_min_df = historical_stock_df.groupby(historical_stock_df.Date.dt.year)[
            'Close'].min().reset_index()
        # Past one year min
        one_year_min_value, one_year_min_date = get_past_min(historical_stock_df, grouped_by_year_historical_min_df, 1)
        past_data_dict[LAST_ONE_YEAR_MIN] = one_year_min_value
        past_data_dict[LAST_ONE_YEAR_MIN_DATE] = one_year_min_date
        past_data_dict[PRICE_DIFF_1YL] = find_difference_from_current_price(one_year_min_value, current_price)
        past_data_dict[DISTANCE_FROM_1YL] = find_difference_from_current_date(one_year_min_date)
        # Past two years min
        two_year_min_value, two_year_min_date = get_past_min(historical_stock_df, grouped_by_year_historical_min_df, 2)
        past_data_dict[LAST_TWO_YEARS_MIN] = two_year_min_value
        past_data_dict[LAST_TWO_YEARS_MIN_DATE] = two_year_min_date
        past_data_dict[PRICE_DIFF_2YL] = find_difference_from_current_price(two_year_min_value, current_price)
        past_data_dict[DISTANCE_FROM_2YL] = find_difference_from_current_date(two_year_min_date)
        # Past three years min
        three_year_min_value, three_year_min_date = get_past_min(historical_stock_df, grouped_by_year_historical_min_df, 3)
        past_data_dict[LAST_THREE_YEARS_MIN] = three_year_min_value
        past_data_dict[LAST_THREE_YEARS_MIN_DATE] = three_year_min_date
        past_data_dict[PRICE_DIFF_3YL] = find_difference_from_current_price(three_year_min_value, current_price)
        past_data_dict[DISTANCE_FROM_3YL] = find_difference_from_current_date(three_year_min_date)
        # Past four years min
        four_year_min_value, four_year_min_date = get_past_min(historical_stock_df, grouped_by_year_historical_min_df, 4)
        past_data_dict[LAST_FOUR_YEARS_MIN] = four_year_min_value
        past_data_dict[LAST_FOUR_YEARS_MIN_DATE] = four_year_min_date
        past_data_dict[PRICE_DIFF_4YL] = find_difference_from_current_price(four_year_min_value, current_price)
        past_data_dict[DISTANCE_FROM_4YL] = find_difference_from_current_date(four_year_min_date)
        # Past five years min
        five_year_min_value, five_year_min_date = get_past_min(historical_stock_df, grouped_by_year_historical_min_df, 5)
        past_data_dict[LAST_FIVE_YEARS_MIN] = five_year_min_value
        past_data_dict[LAST_FIVE_YEARS_MIN_DATE] = five_year_min_date
        past_data_dict[PRICE_DIFF_5YL] = find_difference_from_current_price(five_year_min_value, current_price)
        past_data_dict[DISTANCE_FROM_5YL] = find_difference_from_current_date(five_year_min_date)

        print('Stock Symbol: ' + stock_symbol + ', past max data: ' + str(past_data_dict))
        return past_data_dict
    except Exception as e:
        print('Breakout point calculation failed for stock: ' + stock_symbol + ', due to: ' + str(e))
        raise e
