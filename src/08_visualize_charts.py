"""
Module 8 (part 2): Visualization - Charts
Bar chart comparing suitable habitat area across present/2050/2100
for each species.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs("app/charts", exist_ok=True)

summary = pd.read_csv("data/processed/habitat_loss_summary.csv")
summary = summary[summary["species"] != "green_sea_turtle"]  # unreliable model, excluded from viz

species_names = summary["species"].str.replace("_", " ").str.title()
present = summary["present_suitable_pixels"]
future_2050 = summary["2050_suitable_pixels"]
future_2100 = summary["2100_suitable_pixels"]

x = np.arange(len(species_names))
width = 0.25

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - width, present, width, label="Present", color="#4C72B0")
ax.bar(x, future_2050, width, label="2050", color="#DD8452")
ax.bar(x + width, future_2100, width, label="2100", color="#C44E52")

ax.set_ylabel("Suitable habitat (grid pixels)")
ax.set_title("Predicted Suitable Habitat by Species and Time Period (SSP2-4.5)")
ax.set_xticks(x)
ax.set_xticklabels(species_names, rotation=15)
ax.legend()
plt.tight_layout()

output_path = "app/charts/habitat_comparison.png"
plt.savefig(output_path, dpi=150)
print(f"Saved {output_path}")

# Second chart: % change, which tells the "story" more directly than raw pixel counts
fig2, ax2 = plt.subplots(figsize=(10, 6))
pct_2050 = summary["pct_change_2050"]
pct_2100 = summary["pct_change_2100"]

ax2.bar(x - width/2, pct_2050, width, label="% change by 2050", color="#DD8452")
ax2.bar(x + width/2, pct_2100, width, label="% change by 2100", color="#C44E52")
ax2.axhline(0, color="black", linewidth=0.8)

ax2.set_ylabel("% change in suitable habitat vs. present")
ax2.set_title("Projected Habitat Change by 2050 and 2100 (SSP2-4.5)")
ax2.set_xticks(x)
ax2.set_xticklabels(species_names, rotation=15)
ax2.legend()
plt.tight_layout()

output_path2 = "app/charts/habitat_pct_change.png"
plt.savefig(output_path2, dpi=150)
print(f"Saved {output_path2}")

print("\nModule 8 (charts) complete.")