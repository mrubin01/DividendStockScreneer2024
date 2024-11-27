import yfinance as yf
import pandas as pd


def dict_from_two_lists(lst1: list, lst2: list):
    """
    From two lists it will create a dictionary with keys/values
    :param lst1: a list of keys
    :param lst2: a list of values
    :return: a dictionary
    """
    dictionary = dict(zip(lst1, lst2))

    return dictionary


# Instead of using the function fetch_stock_data, the metrics have been downloaded one
# by one to deal with missing data. The function throws an error even for one missing metric,
# while this way the tickers with missing data will be used as well and the missing metric
# will be set to -999999
def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    try:
        return {
            'ticker': ticker,
            'name': info.get('shortName', ''),
            'dividend_yield': round(info.get('dividendYield', 0) * 100, 2),
            'payout_ratio': round(info.get('payoutRatio', 0), 2),
            'dividend_growth_rate': round(calculate_dividend_growth_rate(stock), 2),
            'eps': round(info.get('trailingEps', 0), 2),
            'pe_ratio': round(info.get('trailingPE', 0), 2),
            'debt_to_equity': round(info.get('debtToEquity', 0), 2),
            'roe': round(info.get('returnOnEquity', 0), 2)
        }
    except KeyError:
        return None


# Function to calculate dividend growth rate
def calculate_dividend_growth_rate(stock):
    """
    It calculates the dividend growth rate using the first and
    the last dividend paid
    :param stock: a yfinance ticker
    :return: if there are at least 2 dividends issued, it will return the increase in dividend per year
    """
    dividends = stock.dividends
    if len(dividends) < 2:
        return 0
    return ((dividends.iloc[-1] / dividends.iloc[0]) ** (1 / len(dividends)) - 1) * 100


# Read stock tickers from a txt file
def read_stock_tickers(stocks):
    with open(stocks, 'r') as file:
        return [line.strip() for line in file]


# Calculate positive and negative metrics
def calculate_metrics(row):
    positives = sum([
        row['dividend_yield'] >= 10,
        0 <= row['payout_ratio'] <= 60,
        row['dividend_growth_rate'] > 5,
        row['eps'] > 0,
        # row['pe_ratio'] < 20,
        row['pe_ratio'] == 1,
        row['debt_to_equity'] < 1,
        # row['roe'] > 10,
        row['roe'] == 1,
        # additional metrics
        row['delta_price_book'] < 0,
        0 <= row['peg_ratio'] <= 1,
        row['div_coverage_ratio'] >= 1.5
    ])
    negatives = 10 - positives
    return positives, negatives




