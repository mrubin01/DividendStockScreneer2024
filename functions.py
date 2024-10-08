import yfinance as yf
import pandas as pd
import numpy
import streamlit


# Function to fetch stock data
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
        row['yearly_dividend_yield'] >= 8,
        0 <= row['payout_ratio'] <= 60,
        row['dividend_growth_rate'] > 5,
        row['eps'] > 0,
        row['pe_ratio'] < 20,
        row['debt_to_equity'] < 1,
        row['roe'] > 10,
        # additional metrics
        row['delta_price_book'] < 0,
        0 <= row['peg_ratio'] <= 1,
        row['div_coverage_ratio'] >= 1.5
    ])
    negatives = 10 - positives
    return positives, negatives




