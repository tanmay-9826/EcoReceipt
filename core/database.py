import pandas as pd

def load_catalog(csv_path):
    # Load the CSV file
    df = pd.read_csv(csv_path)
    
    # 1. Clean the column headers (Removes hidden spaces like " impact_score")
    df.columns = df.columns.str.strip()
    
    # 2. Clean the product names just to be super safe
    if "product" in df.columns:
        df["product"] = df["product"].astype(str).str.strip()
        # Create the normalized column for matching
        df["norm"] = df["product"].str.upper()
    else:
        raise KeyError("The column 'product' was not found in the CSV. Please check your CSV headers.")
        
    return df