import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import load_data
from ui import apply_theme, get_setting, get_setting_bool, render_chart

apply_theme()

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="AI Intelligence Report",
    page_icon="◌",
    layout="wide"
)

st.title("◌ AI Intelligence Report")

st.markdown("""
Generate an AI-assisted intelligence summary from the
Global Terrorism Database (GTD).
""")

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------

df = load_data()

report_format = get_setting("default_report_format", "PDF")
include_charts = get_setting_bool("include_charts", True)
include_tables = get_setting_bool("include_tables", True)

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------

st.sidebar.header("Report Filters")

years = sorted(df["iyear"].unique())

selected_year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + list(years)
)

if selected_year != "All":
    df = df[df["iyear"] == selected_year]

# -------------------------------------------------
# Key Statistics
# -------------------------------------------------

total_incidents = len(df)

total_killed = int(df["nkill"].fillna(0).sum())

total_wounded = int(df["nwound"].fillna(0).sum())

countries = df["country_txt"].nunique()

groups = df["gname"].nunique()

# -------------------------------------------------
# Top Countries
# -------------------------------------------------

top_countries = (
    df["country_txt"]
    .value_counts()
    .head(10)
)

# -------------------------------------------------
# Top Terrorist Groups
# -------------------------------------------------

top_groups = (
    df["gname"]
    .value_counts()
    .head(10)
)

# -------------------------------------------------
# Attack Types
# -------------------------------------------------

attack_types = (
    df["attacktype1_txt"]
    .value_counts()
)

# -------------------------------------------------
# Weapon Types
# -------------------------------------------------

weapon_types = (
    df["weaptype1_txt"]
    .value_counts()
)

# -------------------------------------------------
# Threat Level
# -------------------------------------------------

avg_killed = df["nkill"].fillna(0).mean()

if avg_killed < 2:
    threat = "LOW"

elif avg_killed < 5:
    threat = "MEDIUM"

else:
    threat = "HIGH"

# -------------------------------------------------
# Dashboard Metrics
# -------------------------------------------------

st.subheader("Key Intelligence Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Incidents",
    f"{total_incidents:,}"
)

col2.metric(
    "Fatalities",
    f"{total_killed:,}"
)

col3.metric(
    "Injuries",
    f"{total_wounded:,}"
)

col4.metric(
    "Threat Level",
    threat
)

# -------------------------------------------------
# Executive Summary
# -------------------------------------------------

st.subheader("Executive Summary")

summary = f"""

During the selected period, {total_incidents:,} terrorist incidents
were recorded across {countries} countries.

The attacks resulted in {total_killed:,} fatalities and
{total_wounded:,} injuries.

The overall threat level is assessed as {threat}.

The most affected country is
{top_countries.index[0]}.

The most active terrorist organization is
{top_groups.index[0]}.

The most common attack type is
{attack_types.index[0]}.

The most frequently used weapon is
{weapon_types.index[0]}.

"""

st.info(summary)

if get_setting_bool("enable_report_notifications", False):
    st.toast("AI intelligence report refreshed using the current settings.")

if include_charts:
    # -------------------------------------------------
    # Top Countries
    # -------------------------------------------------
    st.subheader("Top 10 High-Risk Countries")
    fig = px.bar(
        top_countries,
        x=top_countries.values,
        y=top_countries.index,
        orientation="h",
        labels={
            "x":"Incidents",
            "y":"Country"
        }
    )
    render_chart(fig, use_container_width=True)

    # -------------------------------------------------
    # Terrorist Groups
    # -------------------------------------------------
    st.subheader("Most Active Terrorist Groups")
    fig2 = px.bar(
        top_groups,
        x=top_groups.values,
        y=top_groups.index,
        orientation="h",
        labels={
            "x":"Attacks",
            "y":"Group"
        }
    )
    render_chart(fig2, use_container_width=True)

if include_tables:
    st.subheader("High-Risk Table Snapshot")
    st.dataframe(pd.DataFrame({"Country": top_countries.index, "Incidents": top_countries.values}).head(10), use_container_width=True)

# -------------------------------------------------
# AI Intelligence Assessment
# -------------------------------------------------

st.subheader("AI Intelligence Assessment")

recommendation = f"""

1. Increase surveillance in {top_countries.index[0]}.

2. Closely monitor activities associated with
{top_groups.index[0]}.

3. Strengthen protection of infrastructure that
is frequently targeted.

4. Enhance intelligence sharing among agencies.

5. Increase monitoring of explosive-based attacks.

6. Continue trend analysis using predictive
machine learning models.

"""

st.success(recommendation)

# -------------------------------------------------
# Download Report
# -------------------------------------------------

report_sections = [
   "AI INTELLIGENCE REPORT",
   f"Total Incidents : {total_incidents}",
   f"Fatalities : {total_killed}",
   f"Injuries : {total_wounded}",
   f"Threat Level : {threat}",
   f"Top Country : {top_countries.index[0]}",
   f"Top Group : {top_groups.index[0]}",
   f"Most Common Attack : {attack_types.index[0]}",
   f"Most Common Weapon : {weapon_types.index[0]}",
]
if include_charts:
   report_sections.append("Chart Summary: Included")
else:
   report_sections.append("Chart Summary: Excluded")
if include_tables:
   report_sections.append("Table Summary: Included")
else:
   report_sections.append("Table Summary: Excluded")
report_sections.append("Recommendations\n" + recommendation.strip())
report = "\n\n".join(report_sections)

format_extension = {
   "PDF": "pdf",
   "Word": "docx",
   "Text": "txt",
}.get(report_format, "txt")

st.download_button(
   "Download Intelligence Report",
   report,
   file_name=f"AI_Intelligence_Report.{format_extension}",
   mime="text/plain"
)