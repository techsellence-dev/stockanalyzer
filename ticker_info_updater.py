import yfinance as yf

from constants.ticker_constants import MARKET_CAP, FORWARD_PE, TRAILING_PE


def update_ticker_info(stock_symbol):
    ticker = yf.Ticker(stock_symbol)
    try:
        ticker_dict = {MARKET_CAP: str(ticker.info['marketCap'] / 10000000) + ' Cr' if 'marketCap' in ticker.info else 'Not Available',
                       FORWARD_PE: ticker.info['forwardPE'] if 'forwardPE' in ticker.info else 'Not Available',
                       TRAILING_PE: ticker.info['trailingPE'] if 'trailingPE' in ticker.info else 'Not Available'}
        print('Stock Symbol: ' + stock_symbol + ', ticker data: ' + str(ticker_dict))
        return ticker_dict
    except Exception as e:
        print('Failed to download ticker info from yfinance for symbol: ' + stock_symbol +
              ' due to: ' + str(e))
        return {}
