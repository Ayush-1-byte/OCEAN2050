# Ocean 2050 — Climate Refugia for Marine Megafauna

Predicting where endangered marine species (whale sharks, blue whales, humpback whales,
sea turtles, manta rays) will still find habitable ocean conditions as the climate warms.

Uses species occurrence data (OBIS) and marine environmental layers (Bio-ORACLE) to train
species distribution models, then projects habitat suitability to 2050 and 2100 under UN
climate scenarios to identify "climate refugia" — zones worth prioritizing for protection.

## Project structure
- `data/raw/` — untouched downloaded data (OBIS, Bio-ORACLE)
- `data/processed/` — cleaned, ready-to-use datasets
- `src/` — pipeline scripts (numbered by build order)
- `notebooks/` — exploration / scratch work
- `models/` — trained model files
- `app/` — Streamlit dashboard

## Status
Project scaffold created. Data download (Module 1) not yet started.