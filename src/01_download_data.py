"""
Module 1: Data Downloader
Step 1 (today): download ONE species from OBIS to prove the pipeline works.
"""

import requests
import pandas as pd

# OBIS REST API: search occurrence records by scientific name
OBIS_BASE_URL = "https://api.obis.org/v3/occurrence"

def download_species_occurrences(scientific_name: str, size: int = 5000) -> pd.DataFrame:
    """
    Downloads occurrence records (sightings) for one species from OBIS.
    Returns a DataFrame with columns like decimalLatitude, decimalLongitude, eventDate, etc.
    """
    params = {
        "scientificname": scientific_name,
        "size": size
    }
    response = requests.get(OBIS_BASE_URL, params=params)
    response.raise_for_status()  # crash loudly if the request failed

    data = response.json()  
    records = data["results"]

    print(f"Downloaded {len(records)} records for '{scientific_name}'")
    return pd.DataFrame(records)


if __name__ == "__main__":
    # Step 1: just whale shark, just to prove this works
    whale_shark_df = download_species_occurrences("Rhincodon typus")

    # Save to data/raw/ — untouched, exactly as OBIS gave it to us
    whale_shark_df.to_csv("data/raw/whale_shark_occurrences.csv", index=False)

    print(whale_shark_df[["decimalLatitude", "decimalLongitude", "eventDate"]].head())