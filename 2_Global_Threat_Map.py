import streamlit as st
import plotly.graph_objects as go
from data_loader import load_data
from ui import apply_theme, get_mapbox_style, get_setting, get_setting_bool, render_chart

apply_theme()

st.title("◎ Global Threat Map")

df = load_data()

st.sidebar.header("Filters")

year = st.sidebar.selectbox(
    "Year",
    ["All"] + sorted(df["iyear"].unique().tolist())
)

if year != "All":
    df = df[df["iyear"] == year]

df = df.dropna(subset=["latitude", "longitude"]).copy()

map_style = get_mapbox_style(get_setting("map_style", "OpenStreetMap"))

fig = go.Figure()

if get_setting_bool("show_heatmap", False):
    fig.add_trace(
        go.Densitymapbox(
            lat=df["latitude"],
            lon=df["longitude"],
            radius=18,
            colorscale="Greens",
            opacity=0.45,
            hoverinfo="skip",
        )
    )

marker_color = df["nkill"].fillna(0).clip(lower=0, upper=25) if "nkill" in df.columns else None
scatter = go.Scattermapbox(
    lat=df["latitude"],
    lon=df["longitude"],
    mode="markers",
    text=df["country_txt"],
    customdata=df[["city", "gname", "nkill"]].values,
    hovertemplate=(
        "<b>%{text}</b><br>"
        "City: %{customdata[0]}<br>"
        "Group: %{customdata[1]}<br>"
        "Fatalities: %{customdata[2]}<extra></extra>"
    ),
    marker=dict(
        size=9,
        color=marker_color if marker_color is not None else "#4f9a65",
        colorscale="Viridis",
        opacity=0.8,
        line=dict(width=0.5, color="#0d1d12"),
        showscale=False,
    ),
    cluster=dict(color="#2f7d4a", size=18) if get_setting_bool("show_cluster", True) else None,
)
fig.add_trace(scatter)

fig.update_layout(
    mapbox_style=map_style,
    mapbox_center={"lat": 25, "lon": 8},
    mapbox_zoom=1.2,
    margin=dict(l=0, r=0, t=0, b=0),
    height=650,
)

render_chart(fig, use_container_width=True)

st.info(f"Map style: {get_setting('map_style', 'OpenStreetMap')} • Clustering: {'On' if get_setting_bool('show_cluster', True) else 'Off'} • Heatmap: {'On' if get_setting_bool('show_heatmap', False) else 'Off'}")