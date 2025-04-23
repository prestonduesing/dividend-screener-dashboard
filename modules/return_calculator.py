import pandas as pd

def simulate_total_return(data: pd.DataFrame, initial_investment: float = 10000.0,
                          reinvest_dividends: bool = True, compound_freq: str = "Quarterly") -> pd.DataFrame:
    """
    Simulate total return over time with optional dividend reinvestment.
    `compound_freq`: 'Monthly', 'Quarterly', 'Annually'
    """
    data = data.copy()
    shares = initial_investment / data.iloc[0]["Close"]
    total_value = []

    frequency_map = {
        "Monthly": 1,
        "Quarterly": 3,
        "Annually": 12
    }

    compound_every_n = frequency_map.get(compound_freq, 3)
    pending_dividend = 0.0

    for i in range(len(data)):
        row = data.iloc[i]
        div = row["Dividends"]
        price = row["Close"]

        # accumulate dividends
        pending_dividend += (shares * div)

        # compound at selected frequency
        if i % compound_every_n == 0 and i != 0:
            if reinvest_dividends:
                shares += (pending_dividend / price)
            pending_dividend = 0.0

        total_value.append(shares * price)

    data["Total_Value"] = total_value
    return data[["Total_Value"]]
