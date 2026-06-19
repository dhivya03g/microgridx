import pandas as pd

df = pd.read_csv(
    "dataset/household_power_consumption.txt",
    sep=";",
    low_memory=False,
    nrows=5
)

print(df.head())