import streamlit as st
from ui import apply_theme

defaults = {
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
for key, value in defaults.items():
    st.session_state.setdefault(key, value)

st.session_state["display_mode"] = "dark" if st.session_state.get("dark_display", False) else "light"

st.set_page_config(
    page_title="Global Security Intelligence",
    page_icon="S",
    layout="wide"
)

apply_theme()

st.sidebar.markdown("## GSI / DESK")
st.sidebar.caption("Global Security Intelligence")

pages = {
    "Overview": [
        st.Page("1_Home.py", title="Incident overview", icon=":material/home:"),
        st.Page("2_Global_Threat_Map.py", title="Global incident map", icon=":material/public:"),
        st.Page("3_Country_Analysis.py", title="Country analysis", icon=":material/flag:"),
    ],
    "Decision support": [
        st.Page("4_Attack_Prediction.py", title="Attack prediction", icon=":material/psychology:"),
        st.Page("5_Threat_Level.py", title="Threat level", icon=":material/security:"),
        st.Page("6_Forecasting.py", title="Incident forecasting", icon=":material/trending_up:"),
        st.Page("7_AI_Intelligence.py", title="AI intelligence report", icon=":material/smart_toy:"),
    ],
    "Data and controls": [
        st.Page("8_Data_Explorer.py", title="Data explorer", icon=":material/dataset:"),
        st.Page("9_Settings.py", title="Settings", icon=":material/settings:"),
    ],
}

navigation = st.navigation(pages, position="sidebar", expanded=True)
st.sidebar.divider()
st.sidebar.caption("GTD / 1970–2017")
navigation.run()

