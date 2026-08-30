import streamlit as st
import pandas as pd
from data_loader import load_data
from ui import apply_theme

# ----------------------------------------
# Page Configuration
# ----------------------------------------

st.set_page_config(
    page_title="Settings",
    page_icon="⚙",
    layout="wide"
)

st.title("⚙ Dashboard Settings")
st.markdown("Configure your AI-Based Military Intelligence Dashboard.")

DEFAULT_SETTINGS = {
    "dark_display": False,
    "display_mode": "light",
    "dashboard_layout": "Wide",
    "chart_style": "Plotly",
    "default_country": "India",
    "default_forecast_years": 5,
    "minimum_prediction_confidence": 80,
    "map_style": "OpenStreetMap",
    "show_cluster": True,
    "show_heatmap": False,
    "forecast_model": "Linear Regression",
    "prediction_model": "CatBoost",
    "show_prediction_probability": True,
    "show_feature_importance": True,
    "default_report_format": "PDF",
    "include_charts": True,
    "include_tables": True,
    "enable_attack_alerts": True,
    "enable_forecast_alerts": True,
    "enable_report_notifications": False,
}

for key, default in DEFAULT_SETTINGS.items():
    st.session_state.setdefault(key, default)

st.session_state["display_mode"] = "dark" if st.session_state.get("dark_display", False) else "light"

# ----------------------------------------
# Appearance
# ----------------------------------------

st.header("Appearance")

dark_display = st.toggle(
    "Dark display",
    value=bool(st.session_state.get("dark_display", False)),
    key="dark_display",
    help="Switch the main dashboard viewport between green-tinted light and dark modes. This setting persists while you use the dashboard.",
)
st.session_state["display_mode"] = "dark" if dark_display else "light"

layout = st.selectbox(
    "Dashboard Layout",
    ["Wide", "Centered"],
    index=["Wide", "Centered"].index(st.session_state.get("dashboard_layout", "Wide")),
    key="dashboard_layout",
)

chart_style = st.selectbox(
    "Chart Style",
    ["Plotly", "Bar", "Line", "Pie"],
    index=["Plotly", "Bar", "Line", "Pie"].index(st.session_state.get("chart_style", "Plotly")),
    key="chart_style",
)

apply_theme()

# ----------------------------------------
# Default Dashboard Settings
# ----------------------------------------

st.header("Default Dashboard")

country = st.text_input(
    "Default Country",
    value=st.session_state.get("default_country", "India"),
    key="default_country",
)

forecast_years = st.slider(
    "Default Forecast Years",
    1,
    10,
    value=int(st.session_state.get("default_forecast_years", 5)),
    key="default_forecast_years",
)

confidence = st.slider(
    "Minimum Prediction Confidence (%)",
    50,
    100,
    value=int(st.session_state.get("minimum_prediction_confidence", 80)),
    key="minimum_prediction_confidence",
)

# ----------------------------------------
# Map Settings
# ----------------------------------------

st.header("Global Threat Map")

map_style = st.selectbox(
    "Map Style",
    ["OpenStreetMap", "Carto Positron", "Carto Dark"],
    index=["OpenStreetMap", "Carto Positron", "Carto Dark"].index(st.session_state.get("map_style", "OpenStreetMap")),
    key="map_style",
)

show_cluster = st.checkbox(
    "Enable Marker Clustering",
    value=bool(st.session_state.get("show_cluster", True)),
    key="show_cluster",
)

show_heatmap = st.checkbox(
    "Enable Heatmap",
    value=bool(st.session_state.get("show_heatmap", False)),
    key="show_heatmap",
)

# ----------------------------------------
# Forecasting Settings
# ----------------------------------------

st.header("Forecasting")

forecast_model = st.selectbox(
    "Forecasting Algorithm",
    ["Linear Regression", "ARIMA", "Prophet"],
    index=["Linear Regression", "ARIMA", "Prophet"].index(st.session_state.get("forecast_model", "Linear Regression")),
    key="forecast_model",
)

# ----------------------------------------
# Machine Learning Settings
# ----------------------------------------

st.header("Machine Learning")

prediction_model = st.selectbox(
    "Prediction Model",
    ["CatBoost", "Random Forest", "Decision Tree", "Gradient Boosting"],
    index=["CatBoost", "Random Forest", "Decision Tree", "Gradient Boosting"].index(st.session_state.get("prediction_model", "CatBoost")),
    key="prediction_model",
)

show_probability = st.checkbox(
    "Show Prediction Probability",
    value=bool(st.session_state.get("show_prediction_probability", True)),
    key="show_prediction_probability",
)

show_feature_importance = st.checkbox(
    "Show Feature Importance",
    value=bool(st.session_state.get("show_feature_importance", True)),
    key="show_feature_importance",
)

# ----------------------------------------
# Report Settings
# ----------------------------------------

st.header("AI Intelligence Report")

report_format = st.selectbox(
    "Default Report Format",
    ["PDF", "Word", "Text"],
    index=["PDF", "Word", "Text"].index(st.session_state.get("default_report_format", "PDF")),
    key="default_report_format",
)

include_charts = st.checkbox(
    "Include Charts in Report",
    value=bool(st.session_state.get("include_charts", True)),
    key="include_charts",
)

include_tables = st.checkbox(
    "Include Data Tables",
    value=bool(st.session_state.get("include_tables", True)),
    key="include_tables",
)

# ----------------------------------------
# Notifications
# ----------------------------------------

st.header("Notifications")

attack_alerts = st.checkbox(
    "Enable Attack Alerts",
    value=bool(st.session_state.get("enable_attack_alerts", True)),
    key="enable_attack_alerts",
)

forecast_alerts = st.checkbox(
    "Enable Forecast Alerts",
    value=bool(st.session_state.get("enable_forecast_alerts", True)),
    key="enable_forecast_alerts",
)

report_notifications = st.checkbox(
    "Enable Report Notifications",
    value=bool(st.session_state.get("enable_report_notifications", False)),
    key="enable_report_notifications",
)

# ----------------------------------------
# Dataset Information
# ----------------------------------------

st.header("Dataset Information")

try:
    df = load_data()
    st.success("Dataset Loaded Successfully")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Countries", df["country_txt"].nunique())
except Exception:
    st.error("Dataset not found.")

# ----------------------------------------
# Save Settings
# ----------------------------------------

st.divider()

if st.button("Save Settings"):
    st.write("Settings are persisted in the current session.")
    st.success("Settings saved successfully!")

# ----------------------------------------
# Reset Settings
# ----------------------------------------

if st.button("Reset Settings"):
    for key, value in DEFAULT_SETTINGS.items():
        st.session_state[key] = value
    st.session_state["display_mode"] = "dark" if st.session_state.get("dark_display", False) else "light"
    st.success("Settings reset to default values.")
