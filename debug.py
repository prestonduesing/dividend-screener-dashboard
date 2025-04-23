import pandas as pd

# Try reading your mock CSV directly
df = pd.read_csv("data/mock_stock_data.csv")

# Print the first few rows to confirm the file is read correctly
print(df.head())
