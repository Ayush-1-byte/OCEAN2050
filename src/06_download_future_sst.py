"""
Module 6 (part 1): Download future SST projections from Bio-ORACLE.
Using SSP2-4.5 -- a "middle of the road" climate scenario.
"""

import requests

BASE_URL = "https://erddap.bio-oracle.org/erddap/griddap/thetao_ssp245_2020_2100_depthsurf.nc"

# Bio-ORACLE decadal time steps are labeled by the START of each decade.
# 2050 decade = 2050-2059, 2090 decade = 2090-2100 (closest to "2100")
TIME_STEPS = {
    2050: "2050-01-01T00:00:00Z",
    2100: "2090-01-01T00:00:00Z",
}

for label, timestamp in TIME_STEPS.items():
    url = f"{BASE_URL}?thetao_mean[({timestamp})][(-90):(90)][(-180):(180)]"
    output_path = f"data/raw/sst_future_{label}.nc"

    print(f"Downloading {label} SST layer...")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"  -> saved to {output_path}")

print("\nDone.")