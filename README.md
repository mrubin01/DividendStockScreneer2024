# Overview
The original idea for this project comes from Avetik Babayan's Medium page: https://medium.com/insiderfinance/build-a-dividend-stock-screener-with-python-d5ed266c7ec3

It is a screener of dividend stocks showing ten financial metrics. For each metric there are thresholds that are used to highlight it as positive or negative. Apart from the metrics, each stock is identified by: ticker, short name, price, beta.

# Metrics and thresholds

## Delta price - book
The difference between the current price and the book value: if negative, the stock may be undervalued.

## Yearly Dividend Yield
Rather than the current dividend yield, the yearly yield is shown, that is the metric recalculated on a 12-months basis. Stocks with a yearly dividend yield lower than 8% are excluded.

## Payout ratio
This metric must be between 0 and 60% to be considered positive.

## Dividend growth rate
The growth of the dividend issued by the company based on the last 5 years.

## EPS (Earnings per share)
The higher the better, tough the PE ratio is considered more reliable.

## PE Ratio
It is the trailing ratio, not the forward one, and should be compared with the industry average ratio. Anyway, here a PE ratio lower than is considered positive.

## Debt to Equity
It compares the company debts with the equity value. If lower than 1, it is positive.

## ROE (Return On Equity)
A ROE higher than 10% is considered good and the higher the better.

## PEG Ratio
If between 0 and 1, the stock may be undervalued. If higher than 1, the stock may be overvalued. If negative, the stock may be in troubles.

## Dividend coverage
Calculated as the inverse of the payout ratio, it shows the number of times the company can pay dividends to its shareholders. Positive if it's at least 1.5, exceptional if it's above 2.




