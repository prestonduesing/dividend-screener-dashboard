import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def plot_dividend_yield_trend(data: pd.DataFrame, ticker: str):
    """
    Plot dividend yield trend over time using matplotlib and Streamlit.
    """
    if data.empty or "Dividend_Yield" not in data.columns:
        st.warning(f"No data to plot for {ticker}")
        return

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(data.index, data["Dividend_Yield"], marker='o', linestyle='-')
    ax.set_title(f"{ticker} - Dividend Yield Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Dividend Yield")
    ax.grid(True)

    st.pyplot(fig)

from datetime import datetime
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

def plot_dividend_growth(data: pd.DataFrame, ticker: str):
    """
    Plot annual dividend growth rate (excludes incomplete current year).
    """
    if "Dividends" not in data.columns:
        st.warning("No dividend data found.")
        return

    # Resample dividends to yearly totals
    annual_dividends = data["Dividends"].resample("Y").sum()

    # Drop incomplete current year
    if annual_dividends.index[-1].year == datetime.today().year:
        annual_dividends = annual_dividends[:-1]

    # Compute YoY growth %
    growth_rate = annual_dividends.pct_change().dropna() * 100

    if growth_rate.empty:
        st.warning(f"Not enough data to show dividend growth for {ticker}.")
        return

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(growth_rate.index.year, growth_rate.values, color='green')
    ax.set_title(f"{ticker} - Annual Dividend Growth Rate")
    ax.set_ylabel("Growth Rate (%)")
    ax.set_xlabel("Year")
    ax.axhline(0, color='black', linestyle='--')
    st.pyplot(fig)
