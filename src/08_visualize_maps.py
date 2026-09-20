"""
Module 8 (part 1): Visualization - Maps
Generates a Folium map per species per time period, showing predicted
suitable habitat as colored points, plus a refugia map.
"""

import pandas as pd
import folium
import os

SPECIES = ["whale_shark", "blue_whale", "humpback_whale", "manta_ray"]  # skip green_sea_turtle (unreliable model)
PERIODS = ["present", "2050", "2100"]

os.makedirs("app/maps", exist_ok=True)


def make_suitability_map(species, period):
    df = pd.read_csv(f"data/processed/predictions/{species}_{period}.csv")
    suitable = df[df["suitability"] > 0.5]

    m = folium.Map(location=[0, 0], zoom_start=2, tiles="OpenStreetMap")

    # Plotting every point can be slow for large datasets -- sample if huge
    plot_df = suitable.sample(n=min(len(suitable), 3000), random_state=42)

    for _, row in plot_df.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=2,
            color="crimson",
            fill=True,
            fill_opacity=0.5,
            weight=0,
        ).add_to(m)

    output_path = f"app/maps/{species}_{period}.html"
    m.save(output_path)
    print(f"  Saved {output_path} ({len(suitable)} suitable pixels, showing {len(plot_df)})")


def make_refugia_map(species):
    df = pd.read_csv(f"data/processed/predictions/{species}_refugia.csv")

    m = folium.Map(location=[0, 0], zoom_start=2, tiles="CartoDB positron")

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=2,
            color="darkgreen",
            fill=True,
            fill_opacity=0.7,
            weight=0,
        ).add_to(m)

    output_path = f"app/maps/{species}_refugia.html"
    m.save(output_path)
    print(f"  Saved {output_path} ({len(df)} refugia pixels)")


for species in SPECIES:
    print(f"{species}:")
    for period in PERIODS:
        make_suitability_map(species, period)
    make_refugia_map(species)

print("\nModule 8 (maps) complete.")