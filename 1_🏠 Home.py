import streamlit as st
import plotly.express as px
from data_loader import load_data
from ui import apply_theme, page_header, render_chart, section

apply_theme()

page_header("Overview", "Global incident overview", "A compact read of incident volume, human impact, and long-run activity.")

df = load_data()

section("Situation summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Incidents", len(df))
c2.metric("Fatalities", int(df["nkill"].sum()))
c3.metric("Injured", int(df["nwound"].sum()))
c4.metric("Countries", df["country_txt"].nunique())

section("Historical incident volume")

yearly = (
    df.groupby("iyear")
      .size()
      .reset_index(name="Attacks")
)

fig = px.line(
    yearly,
    x="iyear",
    y="Attacks",
    markers=True
)

render_chart(fig, use_container_width=True)

st.caption("Use the navigation panel to move from global patterns into country, model, and forecast views.")