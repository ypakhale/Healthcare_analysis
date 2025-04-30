import json
import pandas as pd
import re
import os

def parse_healthgrades_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    hospitals = []
    
    for state, state_info in data.items():
        cities = state_info.get('cities', {}) or state_info 
        for city, city_info in cities.items():
            for hospital in city_info.get('hospitals', []) or city_info:
                rating = hospital.get('rating', '')
                if rating is not None:
                    rating = rating.replace('%', '')
                
                hospital_data = {
                    'state': state,
                    'city': city,
                    'name': hospital.get('name', ''),
                    'rating': rating
                }
                hospitals.append(hospital_data)
    
    return pd.DataFrame(hospitals)

def parse_medicare_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    if isinstance(data, list):
        records = data
    elif isinstance(data, dict):
        if 'data' in data:
            records = data['data']
        else:
            records = []
            for value in data.values():
                if isinstance(value, list):
                    records.extend(value)
                elif isinstance(value, dict):
                    records.append(value)
    else:
        records = [data]

    medicare_df = pd.DataFrame(records)

    for col in ['payment', 'lower_estimate', 'higher_estimate']:
        if col in medicare_df.columns:
            medicare_df[col] = (
                medicare_df[col]
                .astype(str)
                .str.replace('$', '', regex=False)
                .str.replace(',', '', regex=False)
            )
            medicare_df[col] = pd.to_numeric(medicare_df[col], errors='coerce')
    
    return medicare_df

def standardize_state_names(df, state_column='state'):
    state_mapping = {
        'ALABAMA': 'AL', 'Alabama': 'AL', 'AL': 'AL', 
        'ALASKA': 'AK', 'Alaska': 'AK', 'AK': 'AK',
        'ARIZONA': 'AZ', 'Arizona': 'AZ', 'AZ': 'AZ',
        'ARKANSAS': 'AR', 'Arkansas': 'AR', 'AR': 'AR',
        'CALIFORNIA': 'CA', 'California': 'CA', 'CA': 'CA',
        'COLORADO': 'CO', 'Colorado': 'CO', 'CO': 'CO',
        'CONNECTICUT': 'CT', 'Connecticut': 'CT', 'CT': 'CT',
        'DELAWARE': 'DE', 'Delaware': 'DE', 'DE': 'DE',
        'FLORIDA': 'FL', 'Florida': 'FL', 'FL': 'FL',
        'GEORGIA': 'GA', 'Georgia': 'GA', 'GA': 'GA',
        'HAWAII': 'HI', 'Hawaii': 'HI', 'HI': 'HI',
        'IDAHO': 'ID', 'Idaho': 'ID', 'ID': 'ID',
        'ILLINOIS': 'IL', 'Illinois': 'IL', 'IL': 'IL',
        'INDIANA': 'IN', 'Indiana': 'IN', 'IN': 'IN',
        'IOWA': 'IA', 'Iowa': 'IA', 'IA': 'IA',
        'KANSAS': 'KS', 'Kansas': 'KS', 'KS': 'KS',
        'KENTUCKY': 'KY', 'Kentucky': 'KY', 'KY': 'KY',
        'LOUISIANA': 'LA', 'Louisiana': 'LA', 'LA': 'LA',
        'MAINE': 'ME', 'Maine': 'ME', 'ME': 'ME',
        'MARYLAND': 'MD', 'Maryland': 'MD', 'MD': 'MD',
        'MASSACHUSETTS': 'MA', 'Massachusetts': 'MA', 'MA': 'MA',
        'MICHIGAN': 'MI', 'Michigan': 'MI', 'MI': 'MI',
        'MINNESOTA': 'MN', 'Minnesota': 'MN', 'MN': 'MN',
        'MISSISSIPPI': 'MS', 'Mississippi': 'MS', 'MS': 'MS',
        'MISSOURI': 'MO', 'Missouri': 'MO', 'MO': 'MO',
        'MONTANA': 'MT', 'Montana': 'MT', 'MT': 'MT',
        'NEBRASKA': 'NE', 'Nebraska': 'NE', 'NE': 'NE',
        'NEVADA': 'NV', 'Nevada': 'NV', 'NV': 'NV',
        'NEW HAMPSHIRE': 'NH', 'New Hampshire': 'NH', 'NH': 'NH',
        'NEW JERSEY': 'NJ', 'New Jersey': 'NJ', 'NJ': 'NJ',
        'NEW MEXICO': 'NM', 'New Mexico': 'NM', 'NM': 'NM',
        'NEW YORK': 'NY', 'New York': 'NY', 'NY': 'NY',
        'NORTH CAROLINA': 'NC', 'North Carolina': 'NC', 'NC': 'NC',
        'NORTH DAKOTA': 'ND', 'North Dakota': 'ND', 'ND': 'ND',
        'OHIO': 'OH', 'Ohio': 'OH', 'OH': 'OH',
        'OKLAHOMA': 'OK', 'Oklahoma': 'OK', 'OK': 'OK',
        'OREGON': 'OR', 'Oregon': 'OR', 'OR': 'OR',
        'PENNSYLVANIA': 'PA', 'Pennsylvania': 'PA', 'PA': 'PA',
        'RHODE ISLAND': 'RI', 'Rhode Island': 'RI', 'RI': 'RI',
        'SOUTH CAROLINA': 'SC', 'South Carolina': 'SC', 'SC': 'SC',
        'SOUTH DAKOTA': 'SD', 'South Dakota': 'SD', 'SD': 'SD',
        'TENNESSEE': 'TN', 'Tennessee': 'TN', 'TN': 'TN',
        'TEXAS': 'TX', 'Texas': 'TX', 'TX': 'TX',
        'UTAH': 'UT', 'Utah': 'UT', 'UT': 'UT',
        'VERMONT': 'VT', 'Vermont': 'VT', 'VT': 'VT',
        'VIRGINIA': 'VA', 'Virginia': 'VA', 'VA': 'VA',
        'WASHINGTON': 'WA', 'Washington': 'WA', 'WA': 'WA',
        'WEST VIRGINIA': 'WV', 'West Virginia': 'WV', 'WV': 'WV',
        'WISCONSIN': 'WI', 'Wisconsin': 'WI', 'WI': 'WI',
        'WYOMING': 'WY', 'Wyoming': 'WY', 'WY': 'WY',
        'DISTRICT OF COLUMBIA': 'DC', 'District of Columbia': 'DC', 'DC': 'DC'
    }
    
    if state_column in df.columns:
        df[state_column] = df[state_column].map(lambda x: state_mapping.get(x, x))
    
    return df
