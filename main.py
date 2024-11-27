import yfinance as yf
import pandas as pd
import numpy
import streamlit as st
import sys

import ROEPerIndustry
from functions import *
import PERatioPerIndustry
from datetime import datetime
import time
import warnings
import requests_cache
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)

# GLOBAL VARIABLES
CURRENT_MONTH = datetime.now().month
# industry PE ratios
INDUSTRY_PE_RATIO = PERatioPerIndustry.avg_pe_ratio
# industry ROE
INDUSTRY_ROE = ROEPerIndustry.roe_by_industry
# Dividend yield threshold
DIV_YIELD_THRESHOLD = 10
# Dividend coverage threshold
DIV_COVERAGE_THRESHOLD = 1.5

# the following stocks are updated to Oct 2024 (NASDAQ)
# stocks_list = "nyse_tickers_oct2024.txt"
# stocks_list = "nasdaq_tickers_oct2024.txt"
# stocks.txt comes from the project DataFrom_yfinance (active tickers)

# Ask for a file or a list
Q1_is_right = False
while not Q1_is_right:
    Q1 = input("You want to use a list or a file (file/list)? ")
    if Q1 == "file" or Q1 == "list":
        Q1_is_right = True

# If file, nyse or nasdaq? If list, enter a list of tickers (EG: AAPL,CUBA,MSFT)
Q2_is_right = False
while not Q2_is_right:
    if Q1 == "file":
        Q2 = input("Which exchange (nyse/nasdaq)? ")
        if Q2 == "nyse" or Q2 == "NYSE":
            Q2_is_right = True
            stock_tickers = read_stock_tickers('nyse_tickers_oct2024.txt')
        elif Q2 == "nasdaq" or Q2 == "NASDAQ":
            Q2_is_right = True
            stock_tickers = read_stock_tickers('nasdaq_tickers_oct2024.txt')
    elif Q1 == "list":
        Q2 = input("Enter a list of tickers separated by comma and no space ")
        user_ticker_list = Q2.split(",")
        if isinstance(user_ticker_list, list) and len(user_ticker_list) > 0:
            Q2_is_right = True
            user_ticker_list = Q2.split(",")
            stock_tickers = user_ticker_list

# uncomment the code below to fetch info for a stock
# stock = yf.Ticker("ASC")
# print(stock.info)
# sys.exit()

stock_data = []
stock_with_no_yield = []


# set up a user-agent to avoid error 429 in yfinance (Too many requests): it doesn't fix the error
session = requests_cache.CachedSession('yfinance.cache')
# the user-agent string comes from the developer tool in Firefox
session.headers['User-agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0"


for t in stock_tickers:
    if t not in ("AIF", "AFT"):
        stock = yf.Ticker(t, session=session)
        print(t)
        # this is used to avoid overpassing the request limit per minute
        time.sleep(1)

        try:
            if stock.info["shortName"] and isinstance(stock.info["shortName"], str):
                name = stock.info["shortName"]
            elif stock.info["longName"] and isinstance(stock.info["longName"], str):
                name = stock.info["longName"]
        except KeyError:
            name = "missing"

        try:
            if stock.info["industry"] and isinstance(stock.info["industry"], str):
                industry = stock.info["industry"]
        except KeyError:
            industry = "missing"

        try:
            if stock.info["sector"] and isinstance(stock.info["sector"], str):
                sector = stock.info["sector"]
        except KeyError:
            sector = "missing"

        try:
            if stock.info["beta"] and not isinstance(stock.info["beta"], str):
                beta = round(stock.info["beta"], 2)
        except KeyError:
            beta = -999999

        try:
            if stock.info["currentPrice"] and not isinstance(stock.info["currentPrice"], str):
                price = round(stock.info["currentPrice"], 2)
        except KeyError:
            price = -999999

        # Fetch the metrics, otherwise set them to -999999
        # dividendRate is the total amount of dividends announced for the current year
        # WARNING: sometimes dividendRate is wrong both in yfinance and Nasdaq, but trailingAnnualDividendYield and
        # trailingAnnualDividendRate are wrong most of the time, then it's been decided to use dividendRate to
        # calculate the yield
        try:
            if stock.info["dividendRate"] and not isinstance(stock.info["dividendRate"], str):
                div_rate = round(stock.info["dividendRate"], 2)
        except KeyError:
            div_rate = -999999

        # Forward dividend yield on the basis of dividendRate
        if div_rate != -999999:
            div_yield = round((div_rate / price) * 100, 2)
        else:
            div_yield = -999999

        # If div_yield is below the threshold, go to the next iteration
        if div_yield < DIV_YIELD_THRESHOLD:
            continue

        try:
            if stock.info["payoutRatio"] and not isinstance(stock.info["payoutRatio"], str):
                pay_ratio = round(stock.info["payoutRatio"] * 100, 2)
        except KeyError:
            pay_ratio = -999999

        if pay_ratio != -999999:
            div_coverage = round((1 / pay_ratio) * 100, 2)
        else:
            div_coverage = -999999

        # If div_yield is below the threshold, go to the next iteration
        if div_coverage < DIV_COVERAGE_THRESHOLD:
            continue

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

        # compare the company PE Ratio with the industry avg, otherwise compare it with > or < 20%
        try:
            if pe_ratio != -999999 and pe_ratio < INDUSTRY_PE_RATIO[industry]:
                pe_ratio = 1
            else:
                pe_ratio = 0
        except KeyError:
            if pe_ratio < 20:
                pe_ratio = 1
            else:
                pe_ratio = 0

        try:
            if stock.info["returnOnEquity"] and not isinstance(stock.info["returnOnEquity"], str):
                roe = round(stock.info["returnOnEquity"], 2)
        except KeyError:
            roe = -999999

        # compare the company ROE with the industry avg if possible, otherwise check if it's > 10%
        try:
            if roe != -999999 and roe > INDUSTRY_ROE[industry]:
                roe = 1
            else:
                roe = 0
        except KeyError:
            if roe > 10:
                roe = 1
            else:
                roe = 0

        # additional metrics have been added
        try:
            if stock.info["bookValue"] and not isinstance(stock.info["bookValue"], str):
                book_value = round(stock.info["bookValue"], 2)
        except KeyError:
            book_value = -999999

        delta_price_book = round(float(price) - float(book_value), 2)

        try:
            if stock.info["pegRatio"] and not isinstance(stock.info["pegRatio"], str):
                peg = round(stock.info["pegRatio"], 2)
        except KeyError:
            peg = -999999

        dic = {
            "ticker": t,
            "name": name,
            "industry": industry,
            "sector": sector,
            "beta": beta,
            "price": price,
            "delta_price_book": delta_price_book,
            "dividend_yield": div_yield,
            "payout_ratio": pay_ratio,
            "dividend_growth_rate": div_growth_rate,
            "eps": eps,
            "pe_ratio": pe_ratio,
            "peg_ratio": peg,
            "debt_to_equity": debt_to_equity,
            "roe": roe,
            "div_coverage_ratio": div_coverage
        }

        # exclude stocks with no dividend yield and those with a yearly yield lower than 10%
        try:
            if dic["dividend_yield"] != -999999 and dic["dividend_yield"] >= DIV_YIELD_THRESHOLD and dic["div_coverage_ratio"] >= DIV_COVERAGE_THRESHOLD:
                stock_data.append(dic)
            else:
                stock_with_no_yield.append(dic)
        except KeyError:
            stock_with_no_yield.append(dic)

if len(stock_data) > 0:
    stock_data = [data for data in stock_data if data is not None]  # Filter out stocks with missing data

    # create a dataframe
    stock_df = pd.DataFrame(stock_data)

    stock_df[['positives', 'negatives']] = stock_df.apply(lambda row: calculate_metrics(row), axis=1, result_type="expand")

    # Streamlit interface
    st.title("Dividend Stock Screener")

    st.write("Select sorting criteria:")
    criteria = st.selectbox("Sort by", ["Dividend Yield",
                                        # "Yearly Dividend Yield",
                                        "Payout Ratio",
                                        "Dividend Growth Rate",
                                        "EPS",
                                        "P/E Ratio",
                                        "Debt-to-Equity Ratio",
                                        "ROE",
                                        "positives"])

    sorted_df = stock_df.sort_values(by=criteria.replace(" ", "_").lower(), ascending=False)
    sorted_df = sorted_df.dropna()  # Remove rows with any missing data
    sorted_df = sorted_df.round(2)  # Round to two decimal places


    def highlight_metrics(row):
        colors = []
        for col in sorted_df.columns:
            if col == 'payout_ratio':
                colors.append('background-color: green' if 0 <= row[col] <= 60 else 'background-color: red')
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
            elif col == 'delta_price_book':
                colors.append('background-color: green' if row[col] < 0 else 'background-color: red')
            elif col == 'peg_ratio':
                colors.append('background-color: green' if 0 <= row[col] <= 1 else 'background-color: red')
            elif col == 'div_coverage_ratio':
                colors.append('background-color: green' if row[col] >= 1.5 else 'background-color: red')
            else:
                colors.append('')
        return colors
    # Remove the index column
    st.dataframe(sorted_df.style.apply(highlight_metrics, axis=1))
else:
    print("No stock matches the requirements")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sys.exit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
