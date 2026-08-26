import streamlit as st
from ui import apply_theme

if "display_mode" not in st.session_state:
    st.session_state.display_mode = "light"

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
        st.Page("1_🏠 Home.py", title="Incident overview", icon="🏠"),
        st.Page("2_🌍 Global_Threat_Map.py", title="Global incident map", icon="🌍"),
        st.Page("3_🌎Country_Analysis.py", title="Country analysis", icon="🌎"),
    ],
    "Decision support": [
        st.Page("4_🤖 Attack_Prediction.py", title="Attack prediction", icon="🤖"),
        st.Page("5_🚨Threat_Level.py", title="Threat level", icon="🚨"),
        st.Page("6_📈Forecasting.py", title="Incident forecasting", icon="📈"),
        st.Page("7_🧠 AI_Intelligence.py", title="AI intelligence report", icon="🧠"),
    ],
    "Data and controls": [
        st.Page("8_📊Data_Explorer.py", title="Data explorer", icon="📊"),
        st.Page("9_⚙ Settings.py", title="Settings", icon="⚙️"),
    ],
}

navigation = st.navigation(pages, position="sidebar", expanded=True)
st.sidebar.divider()
st.sidebar.caption("GTD / 1970–2017")
navigation.run()

