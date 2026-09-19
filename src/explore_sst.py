"""
Module 1 (exploration): Open the SST NetCDF file and inspect what's inside.
This is just for understanding the data -- not part of the pipeline itself.
"""

import xarray as xr

ds = xr.open_dataset("data/raw/sst_present.nc")

# Print a summary: dimensions, variables, coordinate ranges
print(ds)

print("\n--- Variables available ---")
print(list(ds.data_vars))

print("\n--- Temperature at a specific point (e.g. off the Philippines coast) ---")
point_temp = ds["thetao_mean"].sel(latitude=10, longitude=125, method="nearest")
print(point_temp.values)