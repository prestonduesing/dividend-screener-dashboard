import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from modules.visualizations import plot_dividend_yield_trend

# Create 50 months of mock data
dates = pd.date_range(end=datetime.today(), periods=50, freq='M')

# Generate mock price and dividend data
mock_data = pd.DataFrame({
    "Close": np.random.uniform(100, 200, size=50),
    "Dividends": np.random.uniform(0.5, 1.5, size=50)
}, index=dates)

# Compute dividend yield
mock_data["Dividend_Yield"] = mock_data["Dividends"] / mock_data["Close"]

# Plot
plot_dividend_yield_trend(mock_data, "MOCK-STOCK")
