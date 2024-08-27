import yfinance as yf
import pandas as pd
import numpy
import streamlit as st
import sys
from functions import *
import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)

# the stock list comes from the project DataFrom_yfinance (active tickers)
stocks_list = "stocks.txt"

# All stocks in a list
stock_tickers = read_stock_tickers('stocks.txt')

# stock_data = [fetch_stock_data(ticker) for ticker in stock_data]

stock_data = []
stock_with_no_yield = []

for t in stock_tickers:
    stock = yf.Ticker(t)

    try:
        if stock.info["shortName"] and isinstance(stock.info["shortName"], str):
            name = stock.info["shortName"]
        elif stock.info["longName"] and isinstance(stock.info["longName"], str):
            name = stock.info["longName"]
    except KeyError:
        name = "missing"

    # Fetch the metrics, otherwise set them to -999999
    try:
        if stock.info["dividendYield"] and not isinstance(stock.info["dividendYield"], str):
            div_yield = round(stock.info["dividendYield"], 2)
    except KeyError:
        div_yield = -999999

    try:
        if stock.info["payoutRatio"] and not isinstance(stock.info["payoutRatio"], str):
            pay_ratio = round(stock.info["payoutRatio"] * 100, 2)
    except KeyError:
        pay_ratio = -999999

    div_growth_rate = round(calculate_dividend_growth_rate(stock), 2)

    try:
        if stock.info["trailingEps"] and not isinstance(stock.info["trailingEps"], str):
            eps = round(stock.info["trailingEps"], 2)
    except KeyError:
        eps = -999999

    try:
        if stock.info["debtToEquity"] and not isinstance(stock.info["debtToEquity"], str):
            debt_to_equity = round(stock.info["debtToEquity"], 2)
    except KeyError:
        debt_to_equity = -999999

    try:
        if stock.info["trailingPE"] and not isinstance(stock.info["trailingPE"], str):
            pe_ratio = round(stock.info["trailingPE"], 2)
    except KeyError:
        pe_ratio = -999999

    try:
        if stock.info["returnOnEquity"] and not isinstance(stock.info["returnOnEquity"], str):
            roe = round(stock.info["returnOnEquity"], 2)
    except KeyError:
        roe = -999999

    dic = {
        "ticker": t,
        "name": name,
        "dividend_yield": div_yield,
        "payout_ratio": pay_ratio,
        "dividend_growth_rate": div_growth_rate,
        "eps": eps,
        "pe_ratio": pe_ratio,
        "debt_to_equity": debt_to_equity,
        "roe": roe
    }

    if dic["dividend_yield"] != -999999:
        stock_data.append(dic)
    else:
        stock_with_no_yield.append(dic)

stock_data = [data for data in stock_data if data is not None]  # Filter out stocks with missing data

# create a dataframe
stock_df = pd.DataFrame(stock_data)

stock_df[['positives', 'negatives']] = stock_df.apply(lambda row: calculate_metrics(row), axis=1, result_type="expand")

# Streamlit interface
st.title("Dividend Stock Screener")

st.write("Select sorting criteria:")
criteria = st.selectbox("Sort by", ["Dividend Yield", "Payout Ratio", "Dividend Growth Rate", "EPS", "P/E Ratio", "Debt-to-Equity Ratio", "ROE", "positives"])

sorted_df = stock_df.sort_values(by=criteria.replace(" ", "_").lower(), ascending=False)
sorted_df = sorted_df.dropna()  # Remove rows with any missing data
sorted_df = sorted_df.round(2)  # Round to two decimal places


def highlight_metrics(row):
    colors = []
    for col in sorted_df.columns:
        if col == 'dividend_yield':
            colors.append('background-color: green' if row[col] > 3 else 'background-color: red')
        elif col == 'payout_ratio':
            colors.append('background-color: green' if 30 <= row[col] <= 60 else 'background-color: red')
        elif col == 'dividend_growth_rate':
            colors.append('background-color: green' if row[col] > 5 else 'background-color: red')
        elif col == 'eps':
            colors.append('background-color: green' if row[col] > 0 else 'background-color: red')
        elif col == 'pe_ratio':
            colors.append('background-color: green' if row[col] < 20 else 'background-color: red')
        elif col == 'debt_to_equity':
            colors.append('background-color: green' if row[col] < 1 else 'background-color: red')
        elif col == 'roe':
            colors.append('background-color: green' if row[col] > 10 else 'background-color: red')
        else:
            colors.append('')
    return colors


# Remove the index column
st.dataframe(sorted_df.style.apply(highlight_metrics, axis=1))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sys.exit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/