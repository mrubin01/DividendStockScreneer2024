# Overview
The original idea for this project comes from Avetik Babayan's Medium page: https://medium.com/insiderfinance/build-a-dividend-stock-screener-with-python-d5ed266c7ec3
It is a screener of dividend stocks showing ten financial metrics. For each metric there are thresholds that are used to highlight it as positive or negative. Apart from the metrics, each stock is identified by: ticker, short name, price, beta.

Based on the 10 financial metrics, each stock will have a score with Positives and Negatives.
Only the stocks with a dividend yield >= 10% and a dividend coverage >= 1.5% will be shown in the final
streamlit chart

# Metrics and thresholds

## Delta price - book
The difference between the current price and the book value: if negative, the stock may be undervalued.

## Forward Dividend Yield
The dividend yield is calculated by using the total amount of dividends announced for the current year (dividendRate).
The threshold to be included in the final view is 10%.

WARNING: sometimes dividendRate is wrong both in yfinance and Nasdaq, but trailingAnnualDividendYield and 
trailingAnnualDividendRate are wrong most of the time, then it's been decided to use dividendRate as the best 
available value. 

## Payout ratio
This metric must be between 0 and 60% to be considered positive.

## Dividend growth rate
The growth of the dividend issued by the company based on the first and the last dividend issued.

## EPS (Earnings per share)
The higher the better, tough the PE ratio is considered more reliable.

## PE Ratio
It is the trailing ratio, not the forward one, and is compared with the industry average ratio.
If it's not possible, it will be positive if it's < 20%: this could imply that the stock is undervalued

## Debt to Equity
It compares the company debts with the equity value. If lower than 1, it is positive.

## ROE (Return On Equity)
It is compared with the industry average ratio.
If it's not possible, it will be positive > 10%

## PEG Ratio
If between 0 and 1, the stock may be undervalued. If higher than 1, the stock may be overvalued. If negative, the stock may be in troubles.

## Dividend coverage
Calculated as the inverse of the payout ratio, it shows the number of times the company can pay dividends to its shareholders. Positive if it's at least 1.5, exceptional if it's above 2.




