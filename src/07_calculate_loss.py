"""
Module 7: Habitat Loss Calculator
For each species: compute % suitable habitat over time, % change,
and identify refugia (pixels suitable in ALL three time periods).
"""

import pandas as pd

SPECIES = ["whale_shark", "blue_whale", "humpback_whale", "manta_ray", "green_sea_turtle"]
PERIODS = ["present", "2050", "2100"]
THRESHOLD = 0.5  # suitability probability above this = "suitable"

summary_rows = []

for species in SPECIES:
    # Load all 3 periods for this species
    dfs = {}
    for period in PERIODS:
        df = pd.read_csv(f"data/processed/predictions/{species}_{period}.csv")
        df["suitable"] = df["suitability"] > THRESHOLD
        dfs[period] = df

    present_area = dfs["present"]["suitable"].sum()
    area_2050 = dfs["2050"]["suitable"].sum()
    area_2100 = dfs["2100"]["suitable"].sum()

    # % change relative to present-day suitable area
    pct_change_2050 = ((area_2050 - present_area) / present_area * 100) if present_area > 0 else float("nan")
    pct_change_2100 = ((area_2100 - present_area) / present_area * 100) if present_area > 0 else float("nan")

    # Refugia: pixel suitable in ALL three periods (same lat/lon grid across files, so we can align by position)
    refugia_mask = dfs["present"]["suitable"].values & dfs["2050"]["suitable"].values & dfs["2100"]["suitable"].values
    refugia_count = refugia_mask.sum()

    refugia_df = dfs["present"].loc[refugia_mask, ["latitude", "longitude"]]
    refugia_df.to_csv(f"data/processed/predictions/{species}_refugia.csv", index=False)

    summary_rows.append({
        "species": species,
        "present_suitable_pixels": present_area,
        "2050_suitable_pixels": area_2050,
        "2100_suitable_pixels": area_2100,
        "pct_change_2050": round(pct_change_2050, 1),
        "pct_change_2100": round(pct_change_2100, 1),
        "refugia_pixels": refugia_count,
    })

    print(f"{species}:")
    print(f"  Present: {present_area} suitable pixels")
    print(f"  2050: {area_2050} ({pct_change_2050:+.1f}%)")
    print(f"  2100: {area_2100} ({pct_change_2100:+.1f}%)")
    print(f"  Refugia (suitable in all 3 periods): {refugia_count} pixels\n")

summary_df = pd.DataFrame(summary_rows)
summary_df.to_csv("data/processed/habitat_loss_summary.csv", index=False)
print("Saved summary to data/processed/habitat_loss_summary.csv")
print(summary_df)