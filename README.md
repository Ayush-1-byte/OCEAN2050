
## Tech Stack

- **Data**: [OBIS API](https://api.obis.org), [Bio-ORACLE](https://bio-oracle.org) (via ERDDAP)
- **Processing**: pandas, numpy, xarray (NetCDF/raster handling)
- **Modeling**: scikit-learn (Logistic Regression, Random Forest)
- **Visualization**: Folium, matplotlib
- **Dashboard**: Streamlit

## Running Locally

```bash
git clone <your-repo-url>
cd OCEAN-2050
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Run the pipeline in order (01 through 08)
python src/01_download_data.py
python src/02_clean_data.py
# ... etc.

# Launch the dashboard
cd app
streamlit run app.py
```

## Limitations

- **Green sea turtle** sample size collapsed from 149 to 5 records during
  environmental extraction, because this species' coastal habitat falls
  outside the resolution of the global SST grid used here. Its model is
  excluded from final results as a result — a known challenge in species
  distribution modeling for coastal species with coarse-resolution
  environmental data.
- Models use **sea surface temperature only** — real habitat suitability
  also depends on food availability, salinity, currents, and reef/coastline
  structure, none of which are included here. Results represent thermal
  suitability, not a complete habitat model.
- Future SST layers use **annual mean values** rather than monthly data, so
  seasonal variation in future scenarios is approximated with a fixed
  mid-year value.
- Projections are based on a single climate scenario (**SSP2-4.5**, a
  "moderate" pathway) — results would differ under more optimistic
  (SSP1-2.6) or severe (SSP5-8.5) scenarios.

## Data Sources & Attribution

- Species occurrence data: [OBIS](https://obis.org), CC0/open data
- Environmental layers: [Bio-ORACLE v3](https://bio-oracle.org), Assis et al.
- Map tiles: OpenStreetMap contributors

## Author

Built by Ayush as part of an independent research project for college
applications, following a self-directed 12-month learning roadmap covering
Python, machine learning, GIS, and climate data analysis.