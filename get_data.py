from utils.cms_api import fetch_cms_hospital_data
from utils.healthgrades_scraper import save_scraped_healthgrades
import shutil

def copy_charges_csv(src_path="charges_data.csv", dest_path="data/raw/charges_data.csv"):
    import os
    os.makedirs("data/raw", exist_ok=True)
    shutil.copyfile(src_path, dest_path)
    print(f"[SUCCESS] charges_data.csv copied to {dest_path}")

if __name__ == "__main__":
    print("=== STARTING DATA DOWNLOAD PIPELINE ===")
    fetch_cms_hospital_data()
    save_scraped_healthgrades()
    copy_charges_csv()
    print("=== ALL DATA SOURCES READY ===")
