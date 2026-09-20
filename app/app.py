"""
Ocean 2050 Dashboard
An interactive Streamlit app showing predicted marine megafauna habitat
suitability, present day and under future climate scenarios (SSP2-4.5).
"""

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Ocean 2050", layout="wide")

SPECIES = ["whale_shark", "blue_whale", "humpback_whale", "manta_ray"]
PERIODS = ["present", "2050", "2100"]


@st.cache_data
def load_predictions(species, period):
    return pd.read_csv(f"../data/processed/predictions/{species}_{period}.csv")


@st.cache_data
def load_refugia(species):
    return pd.read_csv(f"../data/processed/predictions/{species}_refugia.csv")


@st.cache_data
def load_summary():
    df = pd.read_csv("../data/processed/habitat_loss_summary.csv")
    return df[df["species"] != "green_sea_turtle"]


def build_map(df, color="crimson"):
    m = folium.Map(location=[0, 0], zoom_start=1, tiles="OpenStreetMap")
    plot_df = df.sample(n=min(len(df), 3000), random_state=42)
    for _, row in plot_df.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=2, color=color, fill=True, fill_opacity=0.5, weight=0,
        ).add_to(m)
    return m


st.title("🌊 Ocean 2050: Climate Refugia for Marine Megafauna")
st.markdown(
    "Predicting where endangered marine species can still find suitable ocean "
    "conditions as the climate warms, under the SSP2-4.5 scenario."
)

species = st.selectbox("Select a species", SPECIES, format_func=lambda s: s.replace("_", " ").title())

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Species Info", "Current Map", "Future Map", "Loss Chart", "Refugia Map"]
)

with tab1:
    summary = load_summary()
    row = summary[summary["species"] == species].iloc[0]
    st.subheader(species.replace("_", " ").title())
    col1, col2, col3 = st.columns(3)
    col1.metric("Present suitable pixels", int(row["present_suitable_pixels"]))
    col2.metric("2050", int(row["2050_suitable_pixels"]), f"{row['pct_change_2050']:+.1f}%")
    col3.metric("2100", int(row["2100_suitable_pixels"]), f"{row['pct_change_2100']:+.1f}%")
    st.metric("Refugia (suitable across all 3 periods)", int(row["refugia_pixels"]))

with tab2:
    st.subheader(f"Present-day suitable habitat: {species.replace('_', ' ').title()}")
    df = load_predictions(species, "present")
    suitable = df[df["suitability"] > 0.5]
    st_folium(build_map(suitable, "crimson"), width=1100, height=500)

with tab3:
    period = st.radio("Future scenario", ["2050", "2100"], horizontal=True)
    st.subheader(f"{period} suitable habitat: {species.replace('_', ' ').title()}")
    df = load_predictions(species, period)
    suitable = df[df["suitability"] > 0.5]
    st_folium(build_map(suitable, "darkorange"), width=1100, height=500)

with tab4:
    st.subheader("Habitat Comparison Across All Species")
    st.image("charts/habitat_comparison.png")
    st.image("charts/habitat_pct_change.png")

with tab5:
    st.subheader(f"Climate Refugia: {species.replace('_', ' ').title()}")
    st.caption("Areas predicted suitable across present, 2050, AND 2100 -- priority conservation zones.")
    refugia = load_refugia(species)
    if len(refugia) == 0:
        st.warning("No refugia pixels found for this species -- its predicted habitat shifts location entirely rather than persisting in the same place.")
    else:
        st_folium(build_map(refugia, "darkgreen"), width=1100, height=500)

st.caption("Note: green sea turtle excluded from this dashboard due to insufficient training data after coastal SST extraction (see project notes).")