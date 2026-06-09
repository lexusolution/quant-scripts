import os
import json
import pandas as pd

INPUT_DIR = "files"

files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".json")])
week_labels = ["W1", "W2", "W3", "W4"]

call_tables = {}
put_tables = {}

def load_json(path):
    """Load JSON safely even if it's list or double-encoded."""
    with open(path, "r") as f:
        raw = f.read()

    try:
        data = json.loads(raw)
    except:
        data = json.loads(json.loads(raw))

    if isinstance(data, list):
        data = data[0]

    return data

def extract(rows, label, opt_type):
    """Extract strike + lastPrice safely."""
    out = []
    for row in rows:
        strike = row.get("strike")
        last = row.get("lastPrice")
        if strike is not None and last is not None:
            out.append({"strike": strike, f"{label}_{opt_type}": last})
    return pd.DataFrame(out)

for label, filename in zip(week_labels, files):
    path = os.path.join(INPUT_DIR, filename)
    data = load_json(path)

    call_tables[label] = extract(data["calls"], label, "Call")
    put_tables[label] = extract(data["puts"], label, "Put")

final = call_tables["W1"]

for label in week_labels[1:]:
    final = pd.merge(final, call_tables[label], on="strike", how="outer")

for label in week_labels:
    final = pd.merge(final, put_tables[label], on="strike", how="outer")

final.sort_values("strike", inplace=True)

print("\n=== AAL Options Term Structure (Calls then Puts, W1–W4) ===\n")
print(final.to_string(index=False))

