"""
Module 1: Data Downloader
Downloads occurrence records for all 5 target species from OBIS.
"""

import requests
import pandas as pd

OBIS_BASE_URL = "https://api.obis.org/v3/occurrence"

# Scientific names for our 5 target species
SPECIES = {
    "whale_shark": "Rhincodon typus",
    "blue_whale": "Balaenoptera musculus",
    "humpback_whale": "Megaptera novaeangliae",
    "green_sea_turtle": "Chelonia mydas",
    "manta_ray": "Mobula birostris",
}


def download_species_occurrences(scientific_name: str, size: int = 5000) -> pd.DataFrame:
    """Downloads occurrence records (sightings) for one species from OBIS."""
    params = {
        "scientificname": scientific_name,
        "size": size
    }
    response = requests.get(OBIS_BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()
    records = data["results"]

    print(f"Downloaded {len(records)} records for '{scientific_name}'")
    return pd.DataFrame(records)


if __name__ == "__main__":
    for common_name, sci_name in SPECIES.items():
        df = download_species_occurrences(sci_name)
        output_path = f"data/raw/{common_name}_occurrences.csv"
        df.to_csv(output_path, index=False)
        print(f"  -> saved to {output_path}\n")

    print("Module 1 (species data) complete.")