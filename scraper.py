
import requests
from bs4 import BeautifulSoup
import json
import time
import argparse
import os

BASE_URL = "https://www.healthgrades.com"
DIRECTORY_URL = f"{BASE_URL}/hospital-directory"

def get_state_blocks():
    response = requests.get(DIRECTORY_URL)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.select("div[data-qa-target='alpha-list'] ul li")

def scrape(limit=None):
    schema = {}
    total_hospitals = 0
    state_blocks = get_state_blocks()

    for block in state_blocks:
        state_links = block.select("a[data-qa-target$='--title']")
        for state_link in state_links:
            state_name = state_link.text.strip()
            relative_state_url = state_link.get("href")
            state_url = f"{BASE_URL}{relative_state_url}"
            print(f"[INFO] Processing state: {state_name}")
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
                        print(f"  [INFO] Processing city: {city_name}")

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

                                print("    [HOSPITAL FOUND]")
                                print(f"      State  : {state_name}")
                                print(f"      City   : {city_name}")
                                print(f"      Name   : {hospital_name}")
                                print(f"      Rating : {rating}")
                                print(f"      URL    : {hospital_url}")

                                schema[state_name][city_name][hospital_name] = {
                                    "name": hospital_name,
                                    "rating": rating
                                }

                                total_hospitals += 1
                                time.sleep(0.5)

                        except Exception as e:
                            print(f"    [ERROR] Failed to process city '{city_name}': {e}")
                        time.sleep(1)

            except Exception as e:
                print(f"  [ERROR] Failed to process state '{state_name}': {e}")
        time.sleep(1)

    return schema

def main():
    parser = argparse.ArgumentParser(description="Scrape Healthgrades hospital data.")
    parser.add_argument("--scrape", type=int, help="Scrape and print only first N hospital entries.")
    parser.add_argument("--save", type=str, help="Save full dataset to the given path.")
    args = parser.parse_args()

    if args.scrape:
        data = scrape(limit=args.scrape)
        print(json.dumps(data, indent=2))

    elif args.save:
        data = scrape()
        os.makedirs(os.path.dirname(args.save), exist_ok=True)
        with open(args.save, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[INFO] Dataset saved to {args.save}")
    else:
        data = scrape()
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
