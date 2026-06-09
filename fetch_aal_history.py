import yfinance as yf
import os
import json
import pandas as pd
import numpy as np

OUTPUT_DIR = "files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_json_safe(obj):
    """Convert Pandas and NumPy objects to JSON-safe Python types."""
    if isinstance(obj, (pd.Timestamp, pd.Timedelta)):
        return str(obj)
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.ndarray,)):
        return obj.tolist()
    return obj

print("Downloading maximum historical price data for AAL...")

ticker = yf.Ticker("AAL")

# Get full history (max available)
hist = ticker.history(period="max")

# Convert each column using .map() instead of applymap()
for col in hist.columns:
    hist[col] = hist[col].map(convert_json_safe)

# Convert index (dates) to a column
hist.reset_index(inplace=True)
hist["Date"] = hist["Date"].map(convert_json_safe)

# Convert DataFrame to JSON-safe list of dicts
hist_json = hist.to_dict(orient="records")

output_file = os.path.join(OUTPUT_DIR, "aal_history.json")

with open(output_file, "w") as f:
    json.dump(hist_json, f, indent=4)

print(f"Saved historical data to: {output_file}")

