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

ticker = yf.Ticker("AAL")
expirations = ticker.options
next_4 = expirations[:4]

print("Fetching AAL options for the next 4 expirations:")
print(next_4)

for exp in next_4:
    print(f"Downloading options for expiration: {exp}")
    chain = ticker.option_chain(exp)

    # Use DataFrame.map instead of applymap
    calls = chain.calls.map(convert_json_safe).to_dict(orient="records")
    puts = chain.puts.map(convert_json_safe).to_dict(orient="records")

    data = {
        "expiration": exp,
        "calls": calls,
        "puts": puts
    }

    filename = os.path.join(OUTPUT_DIR, f"aal_options_{exp}.json")
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Saved: {filename}")

print("\nDone. Files stored in ./files/")

