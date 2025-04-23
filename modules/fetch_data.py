import yfinance as yf
import pandas as pd

def get_stock_data(ticker: str, period: str = "5y") -> pd.DataFrame:
    """
    Fetch historical price and dividend data for a given ticker.
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, actions=True)
    
    # Ensure 'Dividends' column exists
    if 'Dividends' not in hist.columns:
        hist['Dividends'] = 0.0

    return hist

def get_dividend_yield(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate dividend yield from historical data.
    """
    data = data.copy()
    data['Dividend_Yield'] = data['Dividends'] / data['Close']
    return data[['Close', 'Dividends', 'Dividend_Yield']]
