
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

## Use of AI

Going into this project, I already had a working foundation in Python,
pandas, and basic machine learning concepts from earlier coursework and
personal projects — I wasn't starting from zero on the fundamentals covered
in this project's own learning roadmap. I used Claude (Anthropic) as a
learning aid and pair-programming assistant on top of that foundation,
similar to how many developers now use AI tools professionally.

Specifically:

- **Guidance and sequencing**: Claude helped me break the project down into
  the module-by-module structure above, and walked me through each step in
  order rather than giving me a finished solution upfront.
- **Code**: Claude wrote initial drafts of the pipeline scripts, which I
  then typed into my own IDE, read, understood, ran, and modified myself —
  including changes to file paths, feature choices, and thresholds based on
  what I saw in my own results.
- **Debugging**: A significant part of building this project was fixing real
  errors — working directory issues, an empty `.gitignore`, a broken map
  tile provider, and the green sea turtle sample-size collapse in Module 3.
  In each case, I ran the code, read the actual error message myself, and
  worked through the cause with Claude's help rather than being handed a fix
  with no understanding of why it worked.
- **Explanations**: after each module, Claude explained *why* the code
  worked the way it did (e.g. why pseudo-absences are needed, why
  `month_sin`/`month_cos` exist, why cross-validation matters), and I can
  explain each of these concepts myself, not just point at code that uses them.
- **My own contributions**: I set up and managed the development environment
  (PyCharm, virtual environment, Git/GitHub) myself, ran and tested every
  script, diagnosed real bugs by reading tracebacks myself before asking for
  help, made the calls on how to handle real issues that came up (e.g.
  choosing to document the green sea turtle limitation rather than
  engineering around it), and interpreted the final biological/ecological
  results myself.

I'm disclosing this openly because I believe it's important to be honest
about how AI tools were used in producing this work, and because I think
the process of learning *with* AI — debugging real errors, asking why
something works, and making my own judgment calls on ambiguous results —
was itself a core part of what I learned from this project.

## Future Improvements

Each limitation above has a concrete path to being addressed in a future
version of this project:

| Limitation | Why it happened | How to improve it |
|---|---|---|
| Green sea turtle model unusable (149 → 5 records) | Coastal species' GPS points landed on "land" pixels in the coarse global SST grid during nearest-neighbor extraction | Use a higher-resolution coastal SST product, or search a small radius of nearby ocean pixels instead of only the single nearest one, before falling back to dropping the point |
| Single-scenario projections (SSP2-4.5 only) | Only one climate pathway was downloaded to keep the project scoped | Download and compare SSP1-2.6 (optimistic) and SSP5-8.5 (severe) to show a *range* of possible futures rather than one point estimate — this is standard practice in real climate impact papers |
| Temperature-only habitat model | Simplest environmental variable to start with; other layers add real complexity | Add salinity, pH, chlorophyll (primary productivity/food proxy), and dissolved oxygen from Bio-ORACLE — all downloadable via the same ERDDAP pipeline already built |
| Annual-mean SST, fixed mid-year month | Bio-ORACLE's decadal layers are annual aggregates, not monthly | Use monthly climatology layers if available, so `month_sin`/`month_cos` reflect real seasonal temperature cycles instead of a constant |
| Random Forest only compared to Logistic Regression | Kept the model comparison simple for the first working version | Try gradient boosting (XGBoost/LightGBM) or MaxEnt (the field-standard algorithm for species distribution modeling with presence-only data) |
| Pseudo-absences are uniformly random across the globe | Simplest way to generate negative examples | Restrict pseudo-absence sampling to a plausible "background" region per species (e.g. within a few hundred km of known sightings) — random global absences can make the classification problem artificially easy, inflating AUC |
| Coarse downsampled prediction grid (every 10th pixel) | Kept Module 6 fast enough to run on a laptop | Run full-resolution prediction in chunks/tiles (as the original guide warns is necessary) for a production-quality map, rather than a laptop-friendly demo |
| No uncertainty quantification | Out of scope for first version | Report prediction intervals or model agreement (e.g. how much LogReg and Random Forest disagree) alongside the point predictions, so refugia claims come with a confidence level |

These are presented as a roadmap rather than after-the-fact excuses — each
one is something I understood the cause of at the time (see the module-by-module
build notes above) and consciously chose to defer rather than being unaware of.