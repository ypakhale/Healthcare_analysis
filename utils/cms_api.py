import requests
import json
import os

def fetch_cms_hospital_data(output_path="data/raw/cms_hospital_general.json"):
    DATASET_ID = "c7us-v4mf"
    DATA_URL = f"https://data.cms.gov/provider-data/api/1/datastore/query/{DATASET_ID}/0"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print("[INFO] Fetching CMS Hospital General Information dataset...")
    response = requests.get(DATA_URL)

    if response.status_code == 200:
        data = response.json()
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[SUCCESS] Data saved to {output_path}")
    else:
        raise RuntimeError(f"Failed to fetch CMS data. Status: {response.status_code}")
