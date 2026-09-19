"""
Module 2: Data Cleaner
Cleans all 5 species' raw occurrence data and combines them into one file.
"""

import pandas as pd

SPECIES = ["whale_shark", "blue_whale", "humpback_whale", "green_sea_turtle", "manta_ray"]

KEEP_COLUMNS = ["decimalLatitude", "decimalLongitude", "eventDate"]


def clean_species_file(common_name: str) -> pd.DataFrame:
    df = pd.read_csv(f"data/raw/{common_name}_occurrences.csv")

    before = len(df)

    # Keep only the columns we actually need
    df = df[KEEP_COLUMNS].copy()

    # Drop rows missing lat, lon, or date -- can't use these for modeling
    df = df.dropna(subset=KEEP_COLUMNS)

    # Drop exact duplicate sightings
    df = df.drop_duplicates()

    # Drop physically impossible coordinates
    df = df[(df["decimalLatitude"].between(-90, 90)) &
            (df["decimalLongitude"].between(-180, 180))]

    # Parse date, extract month (needed later for seasonal patterns)
    df["eventDate"] = pd.to_datetime(df["eventDate"], errors="coerce", utc=True)
    df = df.dropna(subset=["eventDate"])  # drop rows where date parsing failed
    df["month"] = df["eventDate"].dt.month

    # Tag every row with which species it belongs to
    df["species"] = common_name

    after = len(df)
    print(f"{common_name}: {before} -> {after} rows ({before - after} removed)")

    return df


if __name__ == "__main__":
    all_species_dfs = [clean_species_file(name) for name in SPECIES]

    combined = pd.concat(all_species_dfs, ignore_index=True)

    output_path = "data/processed/clean_occurrences.csv"
    combined.to_csv(output_path, index=False)

    print(f"\nCombined dataset: {len(combined)} total rows")
    print(f"Saved to {output_path}")
    print("\nRows per species:")
    print(combined["species"].value_counts())