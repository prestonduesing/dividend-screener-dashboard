import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import matplotlib.pyplot as plt

from modules.process_data import load_stock_list, filter_stocks
from modules.visualizations import plot_dividend_yield_trend, plot_dividend_growth
from modules.return_calculator import simulate_total_return

# Set up page
st.set_page_config(page_title="Dividend Screener", layout="wide")
st.title("📈 Dividend Stock Screener & Yield Tracker")

# Sidebar filters
st.sidebar.header("Filter Stocks")
all_stocks = load_stock_list()
sector = st.sidebar.selectbox("Sector", options=["All"] + sorted(all_stocks["Sector"].unique()))
min_yield = st.sidebar.slider("Min Dividend Yield (%)", 0.0, 10.0, 2.0)
max_yield = st.sidebar.slider("Max Dividend Yield (%)", min_yield, 10.0, 7.0)

# Filter stocks
filtered = filter_stocks(all_stocks, sector if sector != "All" else None, min_yield, max_yield)

# Display table
st.subheader("Filtered Dividend Stocks")
st.dataframe(filtered)

# Stock selection — dropdown or manual input
st.subheader("Choose a stock to visualize")
col1, col2 = st.columns([1, 2])
with col1:
    selected_ticker = st.selectbox("Select from filtered stocks", options=filtered["Ticker"])
with col2:
    custom_ticker = st.text_input("Or enter a custom ticker", placeholder="e.g. AAPL")

ticker = custom_ticker.strip().upper() if custom_ticker else selected_ticker

# Generate mock historical dividend data
dates = pd.date_range(end=datetime.today(), periods=50, freq='M')
mock_data = pd.DataFrame({
    "Close": np.random.uniform(80, 200, size=50),
    "Dividends": np.random.uniform(0.4, 1.2, size=50)
}, index=dates)
mock_data["Dividend_Yield"] = mock_data["Dividends"] / mock_data["Close"]

# Plot yield trend
if ticker:
    st.subheader(f"{ticker} Dividend Yield Over Time")
    plot_dividend_yield_trend(mock_data, ticker)

    # Plot growth rate
    st.subheader(f"{ticker} Annual Dividend Growth Rate")
    plot_dividend_growth(mock_data, ticker)

# --- Total Return Simulation ---
st.markdown("## 💰 Total Return Simulation")

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    initial_investment = st.number_input("Initial Investment ($)", value=10000.0, step=1000.0)
with col2:
    compound_freq = st.selectbox("Compounding", ["Quarterly", "Monthly", "Annually"])
with col3:
    reinvest = st.checkbox("Reinvest Dividends?", value=True)

simulate = st.button("Simulate Return")

if simulate:
    simulated = simulate_total_return(mock_data, initial_investment,
                                      reinvest_dividends=reinvest,
                                      compound_freq=compound_freq)

    st.subheader(f"Simulated Growth of ${int(initial_investment):,} in {ticker}")
    st.line_chart(simulated, use_container_width=True)

# --- Additional Visual Insights ---
st.markdown("## 📊 Additional Insights")

if not filtered.empty:
    avg_yield = filtered.groupby("Sector")["DividendYield"].mean().reset_index()
    st.subheader("Average Dividend Yield by Sector")
    st.plotly_chart(px.bar(avg_yield, x="Sector", y="DividendYield", title="Avg Yield by Sector"))

    sector_dist = filtered["Sector"].value_counts().reset_index()
    sector_dist.columns = ["Sector", "Count"]
    st.subheader("Sector Distribution")
    st.plotly_chart(px.pie(sector_dist, values="Count", names="Sector", title="Sector Breakdown"))

    st.subheader("Dividend Yield vs P/E Ratio")
    st.plotly_chart(px.scatter(
        filtered, x="PE_Ratio", y="DividendYield", text="Ticker",
        title="Yield vs. Valuation (P/E)",
        labels={"PE_Ratio": "P/E Ratio", "DividendYield": "Dividend Yield"}
    ))
