import pandas as pd

def load_stock_list() -> pd.DataFrame:
    """
    Return mock stock data as a pandas DataFrame (hardcoded for now).
    """
    data = {
        "Ticker": ["AAPL", "MSFT", "T", "PG", "XOM", "JNJ", "KO", "VZ", "PFE", "D"],
        "Company": ["Apple Inc.", "Microsoft Corp.", "AT&T Inc.", "Procter & Gamble", "Exxon Mobil", 
                    "Johnson & Johnson", "Coca-Cola", "Verizon", "Pfizer Inc.", "Dominion Energy"],
        "Sector": ["Technology", "Technology", "Telecom", "Consumer Staples", "Energy", 
                   "Healthcare", "Consumer Staples", "Telecom", "Healthcare", "Utilities"],
        "DividendYield": [0.55, 0.88, 6.90, 2.46, 3.21, 2.96, 3.05, 6.47, 4.35, 5.23],
        "PE_Ratio": [28.9, 33.1, 7.8, 25.5, 10.3, 17.4, 22.2, 8.1, 11.6, 15.2]
    }
    return pd.DataFrame(data)

def filter_stocks(data: pd.DataFrame, sector: str = None, min_yield: float = 0.0, max_yield: float = 10.0) -> pd.DataFrame:
    """
    Filter stocks by sector and dividend yield range.
    """
    filtered = data[
        (data["DividendYield"] >= min_yield) &
        (data["DividendYield"] <= max_yield)
    ]
    if sector:
        filtered = filtered[filtered["Sector"] == sector]

    return filtered.sort_values(by="DividendYield", ascending=False)
