import os
import json
import pandas as pd

def merge_hospital_data(cms_path, healthgrades_path, output_path="data/processed/combined_hospital_data.csv"):
    print("[INFO] Parsing CMS and Healthgrades datasets...")

    cms_df = parse_medicare_json(cms_path)
    hg_df = parse_healthgrades_json(healthgrades_path)

    hg_df = standardize_state_names(hg_df)
    cms_df = standardize_state_names(cms_df, state_column='state')

    combined = pd.merge(
        cms_df,
        hg_df,
        how='left',
        on=['state', 'city']
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    combined.to_csv(output_path, index=False)
    print(f"[SUCCESS] Combined hospital data saved to {output_path}")
    return combined

def merge_with_charges(combined_df_path, charges_path="data/raw/charges_data.csv", output_path="data/processed/merged_healthcare_data.csv"):
    print("[INFO] Loading combined hospital data and charges...")

    df = pd.read_csv(combined_df_path)
    charges = pd.read_csv(charges_path, encoding="latin1")

    df = df.rename(columns={
        'facility_id': 'Rndrng_Prvdr_CCN',
        'facility_name': 'facility_name_full',
        'citytown': 'facility_city',
        'state': 'facility_state',
        'zip_code': 'facility_zip'
    })

    df['Rndrng_Prvdr_CCN'] = df['Rndrng_Prvdr_CCN'].astype(str)
    charges['Rndrng_Prvdr_CCN'] = charges['Rndrng_Prvdr_CCN'].astype(str)

    merged = charges.merge(df, on='Rndrng_Prvdr_CCN', how='left', suffixes=('_provider', '_facility'))
    merged = merged.dropna(axis=1, how='all')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    merged.to_csv(output_path, index=False)
    print(f"[SUCCESS] Final merged dataset saved to {output_path}")


def main():
    cms_path = "data/raw/cms_hospital_general.json"
    healthgrades_path = "data/raw/healthgrades_data.json"
    combined_path = "data/processed/combined_hospital_data.csv"

    merge_hospital_data(cms_path, healthgrades_path, combined_path)
    merge_with_charges(combined_path)

if __name__ == "__main__":
    main()