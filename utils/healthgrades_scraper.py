import requests
from bs4 import BeautifulSoup
import json
import os
import time

BASE_URL = "https://www.healthgrades.com"
DIRECTORY_URL = f"{BASE_URL}/hospital-directory"

def scrape_healthgrades(limit=None):
    schema = {}
    total_hospitals = 0

    def get_state_blocks():
        response = requests.get(DIRECTORY_URL)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.select("div[data-qa-target='alpha-list'] ul li")

    state_blocks = get_state_blocks()

    for block in state_blocks:
        state_links = block.select("a[data-qa-target$='--title']")
        for state_link in state_links:
            state_name = state_link.text.strip()
            relative_state_url = state_link.get("href")
            state_url = f"{BASE_URL}{relative_state_url}"
            schema[state_name] = {}

            try:
                state_response = requests.get(state_url)
                state_soup = BeautifulSoup(state_response.content, "html.parser")
                city_section = state_soup.select_one("section[data-qa-target='top-cities-list']")

                if city_section:
                    city_links = city_section.select("a.sAL3j1mOy0qvcbNn")
                    for city_link in city_links:
                        city_name = city_link.text.strip()
                        relative_city_url = city_link.get("href")
                        city_url = f"{BASE_URL}/hospital-directory/{relative_city_url}"
                        schema[state_name][city_name] = {}

                        try:
                            city_response = requests.get(city_url)
                            city_soup = BeautifulSoup(city_response.content, "html.parser")
                            hospital_links = city_soup.find_all(
                                "a", attrs={"data-qa-target": "name-link"})

                            for hospital_link in hospital_links:
                                if limit and total_hospitals >= limit:
                                    return schema

                                hospital_name = hospital_link.text.strip()
                                hospital_href = hospital_link.get("href")
                                hospital_url = f"{BASE_URL}/{hospital_href}"

                                try:
                                    hosp_resp = requests.get(hospital_url)
                                    hosp_soup = BeautifulSoup(hosp_resp.content, "html.parser")
                                    coin_elements = hosp_soup.find_all(
                                        "div",
                                        class_="hospital-patient-experience-coin-circle hospital-patient-experience-coin-circle-non-sponsored"
                                    )
                                    rating = coin_elements[1].get_text(strip=True) if len(coin_elements) > 1 else None
                                except Exception:
                                    rating = None

                                schema[state_name][city_name][hospital_name] = {
                                    "name": hospital_name,
                                    "rating": rating
                                }

                                total_hospitals += 1
                                time.sleep(0.5)

                        except Exception:
                            continue
                        time.sleep(1)

            except Exception:
                continue
        time.sleep(1)

    return schema

def save_scraped_healthgrades(output_path="data/raw/healthgrades_data.json", limit=None):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    data = scrape_healthgrades(limit=limit)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[SUCCESS] Scraped data saved to {output_path}")
