import os
import json

INPUT_DIR = "files"

files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".json")])

if not files:
    print("No option files found in ./files/")
    exit()

for filename in files:
    path = os.path.join(INPUT_DIR, filename)
    print(f"\n=== Reading {filename} ===")

    with open(path, "r") as f:
        data = json.load(f)

    print(f"Expiration: {data['expiration']}")
    print(f"Number of Calls: {len(data['calls'])}")
    print(f"Number of Puts: {len(data['puts'])}")

    print("\nSample Calls (first 5):")
    for c in data["calls"][:5]:
        print(c)

    print("\nSample Puts (first 5):")
    for p in data["puts"][:5]:
        print(p)

