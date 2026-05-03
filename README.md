# Quantifying Market Risk

This project analyzes financial market risk using Python and historical data from the S&P 500 (SPY ETF). The goal is to model volatility and quantify potential losses using commonly applied risk measures.
This project was independently developed as part of my studies in actuarial science and financial engineering.

 Overview

The analysis includes:

- Computation of simple and log returns from market prices  
- Estimation of volatility using:
  - Historical (rolling window) approach  
  - Exponentially Weighted Moving Average (EWMA)  
- Risk measurement using:
  - Parametric Value-at-Risk (VaR)  
  - Historical Value-at-Risk  
  - Expected Shortfall (ES)  

The results highlight the differences between model-based and data-driven approaches, as well as the trade-off between stability and responsiveness in volatility estimation.

Tools Used

- Python (pandas, numpy, matplotlib, yfinance)  
- Excel (for output and visualization)

Key Insights

- EWMA volatility reacts faster to market shocks compared to historical volatility  
- Parametric VaR is smoother and more responsive, while historical VaR reflects past extreme events  
- Expected Shortfall provides a more complete measure of downside risk by capturing tail losses  

Project Structure

- `risk_model.py` – main Python script  
- `report.pdf` – written explanation of the methodology and results
- `market_data.xlx` - excel file 
