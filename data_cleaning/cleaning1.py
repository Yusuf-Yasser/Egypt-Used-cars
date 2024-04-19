import pandas as pd
import numpy as np
import os

# Load the data into a DataFrame
df = pd.read_csv("../data/raw_contactcars_data.csv")

# Replace spaces in column names with underscores
df.columns = df.columns.str.replace(" ", "_")

# Turn the column names into lowercase
df.columns = df.columns.str.lower()

# Clean up the mileage column
df["mileage"] = df["mileage"].str.replace(",", "").astype(float)

# Clean up the price column
df["price"] = df["price"].str.replace(",", "").astype(float)

# Clean up the minimum_down_payment column
df["minimum_down_payment"] = df["minimum_down_payment"].replace(
    "no minimum down payment specified", np.nan
)
df["minimum_down_payment"] = (
    df["minimum_down_payment"].str.replace(",", "").astype(float)
)

# find outliers in the mileage column then remove them
mileage_mean = df["mileage"].mean()
mileage_std = df["mileage"].std()
mileage_cutoff = mileage_std * 3
mileage_lower, mileage_upper = (
    mileage_mean - mileage_cutoff,
    mileage_mean + mileage_cutoff,
)
df = df[(df["mileage"] > mileage_lower) & (df["mileage"] < mileage_upper)]

# find outliers in the price column then remove them
price_mean = df["price"].mean()
price_std = df["price"].std()
price_cutoff = price_std * 3
price_lower, price_upper = price_mean - price_cutoff, price_mean + price_cutoff
df = df[(df["price"] > price_lower) & (df["price"] < price_upper)]


# Save df to a SQL database
database_path = "../data/contactcars.db"

# Check if database file already exists and remove it
if os.path.exists(database_path):
    os.remove(database_path)

# Save df to a SQL database
df.to_sql("contactcars", f"sqlite:///{database_path}", index=False)

# Save df to a CSV file
csv_path = "../data/contactcars.csv"
df.to_csv(csv_path, index=False)
