
import requests
import json
import os

# Dataset ID and API URL
DATASET_ID = "c7us-v4mf"
DATA_URL = f"https://data.cms.gov/provider-data/api/1/datastore/query/{DATASET_ID}/0"

# Output path
os.makedirs("data/raw", exist_ok=True)
output_path = "data/raw/cms_hospital_general.json"

# Fetch data
print("[INFO] Fetching CMS Hospital General Information dataset...")
response = requests.get(DATA_URL)

if response.status_code == 200:
    data = response.json()
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[SUCCESS] Data saved to {output_path}")
else:
    print(f"[ERROR] Failed to fetch data. Status code: {response.status_code}")