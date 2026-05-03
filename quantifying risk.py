import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

#download market data
ticker = "SPY"
data = yf.download(ticker, start="2020-01-01", auto_adjust=True)

print(data.head())
print(data.columns)


prices = data["Close"].copy()

#calculate returns

simple_returns = prices.pct_change().dropna()

log_returns = np.log(prices / prices.shift(1)).dropna()

print("\nFirst simple returns:")
print(simple_returns.head())

print("\nFirst log returns:")
print(log_returns.head())

#historical volatility
trading_days = 252
hist_window = 30

hist_vol = log_returns.rolling(window=hist_window).std() * np.sqrt(trading_days)

print("\nHistorical volatility:")
print(hist_vol.tail())

#EWMA volatility
lambda_ = 0.94

ewma_var = pd.Series(index=log_returns.index, dtype=float)
ewma_var.iloc[0] = log_returns.iloc[0] ** 2

for t in range(1, len(log_returns)):
    ewma_var.iloc[t] = (
        lambda_ * ewma_var.iloc[t - 1]
        + (1 - lambda_) * (log_returns.iloc[t - 1] ** 2)
    )

ewma_vol = np.sqrt(ewma_var) * np.sqrt(trading_days)

print("\nEWMA volatility:")
print(ewma_vol.tail())

#parametric VaR
confidence_level = 0.95
z = 1.65  # approximate z-score for 95%

VaR = -z * ewma_vol / np.sqrt(trading_days)

print("\nParametric VaR:")
print(VaR.tail())

#historical VaR
var_window = 250
hist_VaR = log_returns.rolling(window=var_window).quantile(0.05)

print("\nHistorical VaR:")
print(hist_VaR.tail())

#historical ES
ES_hist = log_returns.rolling(window=var_window).apply(
    lambda x: x[x <= x.quantile(0.05)].mean()
)

print("\nHistorical ES:")
print(ES_hist.tail())

#combine into one data frame
df = pd.concat(
    [
        prices,
        simple_returns,
        log_returns,
        hist_vol,
        ewma_vol,
        VaR,
        hist_VaR,
        ES_hist,
    ],
    axis=1,
)

df.columns = [
    "Price",
    "Simple Return",
    "Log Return",
    "Historical Volatility",
    "EWMA Volatility",
    "VaR (Parametric 95%)",
    "VaR (Historical 95%)",
    "ES (Historical 95%)",
]

#export to Excel
df.to_excel("market_data.xlsx")
print("\nData saved to Excel!")

#plots
# volatility comparison
plt.figure(figsize=(12, 6))
plt.plot(hist_vol, label="Historical Volatility")
plt.plot(ewma_vol, label="EWMA Volatility")
plt.title("Historical vs EWMA Volatility")
plt.xlabel("Date")
plt.ylabel("Annualized Volatility")
plt.legend()
plt.grid(True)
plt.show()

# VaR
plt.figure(figsize=(12, 6))
plt.plot(VaR, label="VaR (Parametric 95%)")
plt.title("Value-at-Risk (EWMA Based)")
plt.xlabel("Date")
plt.ylabel("VaR")
plt.legend()
plt.grid(True)
plt.show()

# VaR comparison
plt.figure(figsize=(12, 6))
plt.plot(VaR, label="Parametric VaR")
plt.plot(hist_VaR, label="Historical VaR")
plt.title("VaR Comparison")
plt.xlabel("Date")
plt.ylabel("VaR")
plt.legend()
plt.grid(True)
plt.show()

# VaR vs ES
plt.figure(figsize=(12, 6))
plt.plot(hist_VaR, label="Historical VaR")
plt.plot(ES_hist, label="Historical ES")
plt.title("VaR vs Expected Shortfall")
plt.xlabel("Date")
plt.ylabel("Risk Measure")
plt.legend()
plt.grid(True)
plt.show()