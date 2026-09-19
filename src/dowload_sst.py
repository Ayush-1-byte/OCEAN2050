"""
Module 1 (part 2): Download present-day Sea Surface Temperature from Bio-ORACLE.
Uses Bio-ORACLE's public ERDDAP server (no account/API key needed).
"""

import requests

# Bio-ORACLE ERDDAP griddap endpoint for Ocean Temperature (surface depth)
# We're requesting the "mean" temperature statistic, most recent time step, full global grid
ERDDAP_URL = (
    "https://erddap.emodnet.eu/erddap/griddap/biooracle_ot_ds.nc"
    "?thetao_mean[(2010-01-01T00:00:00Z)][(-90):(90)][(-180):(180)]"
)

OUTPUT_PATH = "data/raw/sst_present.nc"

def download_sst_layer():
    print("Requesting SST layer from Bio-ORACLE ERDDAP server...")
    response = requests.get(ERDDAP_URL, stream=True)
    response.raise_for_status()

    with open(OUTPUT_PATH, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    download_sst_layer()