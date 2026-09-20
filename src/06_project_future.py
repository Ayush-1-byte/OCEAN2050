"""
Module 6 (part 2): Future Projector
Applies each species' trained model to present-day, 2050, and 2100
SST grids to predict habitat suitability across the whole ocean.
"""

import numpy as np
import pandas as pd
import xarray as xr
import joblib
import os

SPECIES = ["whale_shark", "blue_whale", "humpback_whale", "manta_ray", "green_sea_turtle"]

# Downsample factor: take every Nth grid point in each direction.
# Keeps prediction fast; still gives global coverage.
DOWNSAMPLE = 10

SST_FILES = {
    "present": "data/raw/sst_present.nc",
    "2050": "data/raw/sst_future_2050.nc",
    "2100": "data/raw/sst_future_2100.nc",
}


def load_sst_grid(path):
    ds = xr.open_dataset(path)
    layer = ds["thetao_mean"]
    if "time" in layer.dims:
        layer = layer.isel(time=0)
    # Downsample
    layer = layer.isel(
        latitude=slice(0, None, DOWNSAMPLE),
        longitude=slice(0, None, DOWNSAMPLE),
    )
    return layer


def build_feature_table(sst_layer):
    """Turn a 2D lat/lon SST grid into a flat table of features, one row per pixel."""
    lats = sst_layer["latitude"].values
    lons = sst_layer["longitude"].values
    sst_values = sst_layer.values  # shape: (n_lat, n_lon)

    lon_grid, lat_grid = np.meshgrid(lons, lats)  # both shape: (n_lat, n_lon)

    df = pd.DataFrame({
        "latitude": lat_grid.ravel(),
        "longitude": lon_grid.ravel(),
        "sst": sst_values.ravel(),
    })

    df = df.dropna(subset=["sst"])  # drop land pixels

    # Use a fixed "mid-year" month since these are annual mean layers, not monthly
    fixed_month = 6
    df["sst_sq"] = df["sst"] ** 2
    df["month_sin"] = np.sin(2 * np.pi * fixed_month / 12)
    df["month_cos"] = np.cos(2 * np.pi * fixed_month / 12)
    df["lat_abs"] = df["latitude"].abs()

    return df


FEATURES = ["sst", "sst_sq", "month_sin", "month_cos", "lat_abs"]

os.makedirs("data/processed/predictions", exist_ok=True)

for species in SPECIES:
    print(f"\n=== {species} ===")
    model = joblib.load(f"models/{species}_model.pkl")
    scaler = joblib.load(f"models/{species}_scaler.pkl")

    for period, path in SST_FILES.items():
        sst_layer = load_sst_grid(path)
        feature_table = build_feature_table(sst_layer)

        X = feature_table[FEATURES]
        X_scaled = scaler.transform(X)

        probabilities = model.predict_proba(X_scaled)[:, 1]  # probability of "presence"
        feature_table["suitability"] = probabilities

        output_path = f"data/processed/predictions/{species}_{period}.csv"
        feature_table[["latitude", "longitude", "sst", "suitability"]].to_csv(output_path, index=False)

        suitable_fraction = (probabilities > 0.5).mean()
        print(f"  {period}: {len(feature_table)} pixels predicted, "
              f"{suitable_fraction:.1%} classified suitable, saved to {output_path}")

print("\nModule 6 complete.")