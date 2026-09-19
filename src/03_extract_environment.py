"""
Module 3: Environment Extractor
For every animal sighting, look up the sea surface temperature at that
exact lat/lon and attach it as a new column.
"""

import pandas as pd
import xarray as xr

occurrences = pd.read_csv("data/processed/clean_occurrences.csv")

sst = xr.open_dataset("data/raw/sst_present.nc")

print("SST dataset dimensions:", dict(sst.dims))

sst_layer = sst["thetao_mean"]

# If there's a leftover time dimension, collapse it to a single 2D lat/lon grid
if "time" in sst_layer.dims:
    sst_layer = sst_layer.isel(time=0)

print(f"\nExtracting SST for {len(occurrences)} sightings...")

lats = xr.DataArray(occurrences["decimalLatitude"].values, dims="points")
lons = xr.DataArray(occurrences["decimalLongitude"].values, dims="points")

sampled = sst_layer.sel(latitude=lats, longitude=lons, method="nearest")

# Force to a flat 1D array matching the number of rows
occurrences["sst"] = sampled.values.reshape(-1)

missing_sst = occurrences["sst"].isna().sum()
print(f"Sightings with no SST match (likely coastal/land pixels): {missing_sst}")

occurrences = occurrences.dropna(subset=["sst"])

output_path = "data/processed/occurrences_with_sst.csv"
occurrences.to_csv(output_path, index=False)

print(f"\nFinal dataset: {len(occurrences)} rows")
print(f"Saved to {output_path}")
print("\nSST summary by species:")
print(occurrences.groupby("species")["sst"].mean())