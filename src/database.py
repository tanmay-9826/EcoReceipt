import pandas as pd

def load_catalog(csv_path="data/products.csv"):
    df = pd.read_csv(csv_path)
    df["norm"] = df["product"].str.upper()
    return df
