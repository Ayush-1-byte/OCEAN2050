"""
Module 4: Feature Engineer
Adds derived features and generates pseudo-absence points so the model
has both positive (sighted) and negative (assumed absent) examples.
"""

import numpy as np
import pandas as pd
import xarray as xr

# ---- Load presence data (real sightings + SST) ----
presences = pd.read_csv("data/processed/occurrences_with_sst.csv")
presences["presence"] = 1

# ---- Load SST grid ----
sst = xr.open_dataset("data/raw/sst_present.nc")
sst_layer = sst["thetao_mean"]
if "time" in sst_layer.dims:
    sst_layer = sst_layer.isel(time=0)

# Pull out raw numpy arrays -- much faster than repeated xarray .sel() calls
grid_lats = sst_layer["latitude"].values
grid_lons = sst_layer["longitude"].values
grid_values = sst_layer.values  # 2D array: [lat, lon]


def fast_nearest_lookup(query_lats, query_lons):
    """Manually find nearest grid cell for each point using np.searchsorted (fast)."""
    lat_idx = np.searchsorted(grid_lats, query_lats)
    lon_idx = np.searchsorted(grid_lons, query_lons)
    lat_idx = np.clip(lat_idx, 0, len(grid_lats) - 1)
    lon_idx = np.clip(lon_idx, 0, len(grid_lons) - 1)
    return grid_values[lat_idx, lon_idx]


# ---- Generate pseudo-absences ----
np.random.seed(42)
n_absences = len(presences)

random_lats = np.random.uniform(-90, 90, size=n_absences * 3)
random_lons = np.random.uniform(-180, 180, size=n_absences * 3)

print("Looking up SST for random points...")
random_sst = fast_nearest_lookup(random_lats, random_lons)

absences = pd.DataFrame({
    "decimalLatitude": random_lats,
    "decimalLongitude": random_lons,
    "sst": random_sst,
})
absences = absences.dropna(subset=["sst"])
absences = absences.sample(n=n_absences, random_state=42)
absences["presence"] = 0
absences["species"] = "pseudo_absence"
absences["month"] = np.random.randint(1, 13, size=len(absences))

# ---- Combine presences + absences ----
combined = pd.concat([presences, absences], ignore_index=True)

# ---- Derived features ----
combined["sst_sq"] = combined["sst"] ** 2
combined["month_sin"] = np.sin(2 * np.pi * combined["month"] / 12)
combined["month_cos"] = np.cos(2 * np.pi * combined["month"] / 12)
combined["lat_abs"] = combined["decimalLatitude"].abs()

output_path = "data/processed/training_data.csv"
combined.to_csv(output_path, index=False)

print(f"Presences: {len(presences)}")
print(f"Pseudo-absences: {len(absences)}")
print(f"Total training rows: {len(combined)}")
print(f"Saved to {output_path}")
print("\nClass balance:")
print(combined["presence"].value_counts())