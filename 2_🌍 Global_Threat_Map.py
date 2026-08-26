import streamlit as st
import plotly.express as px
from data_loader import load_data
from ui import apply_theme, render_chart

apply_theme()

st.title("🌍 Global Threat Map")

df = load_data()

st.sidebar.header("Filters")

year = st.sidebar.selectbox(
    "Year",
    ["All"] + sorted(df["iyear"].unique().tolist())
)

if year != "All":
    df = df[df["iyear"] == year]

df = df.dropna(subset=["latitude", "longitude"])

fig = px.scatter_geo(
    df,
    lat="latitude",
    lon="longitude",
    color="attacktype1_txt",
    hover_name="country_txt",
    hover_data=["city", "gname", "nkill"],
    projection="natural earth"
)

render_chart(fig, use_container_width=True)

st.info("👈 Change filters from the sidebar.")