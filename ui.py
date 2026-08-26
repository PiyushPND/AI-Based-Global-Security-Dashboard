import streamlit as st


def get_setting(name: str, default):
    return st.session_state.get(name, default)


def render_chart(figure, **kwargs) -> None:
    """Render charts with the style selected in Settings."""
    chart_style = get_setting("chart_style", "Plotly")
    palettes = {
        "Plotly": ["#357a4a", "#6b8f71", "#b56b17", "#315b75"],
        "Bar": ["#315b75", "#357a4a", "#b56b17", "#7b4f78"],
        "Line": ["#357a4a", "#b56b17", "#315b75", "#7b4f78"],
        "Pie": ["#357a4a", "#6b8f71", "#b56b17", "#315b75"],
    }
    figure.update_layout(
        template="plotly_dark" if get_setting("display_mode", "light") == "dark" else "plotly_white",
        colorway=palettes.get(chart_style, palettes["Plotly"]),
        font={"family": "DM Sans, sans-serif"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(figure, **kwargs)


def apply_theme() -> None:
    dark_display = st.session_state.get("display_mode", "light") == "dark"
    ink = "#e3eee1" if dark_display else "#1c2b1d"
    muted = "#a7b9a5" if dark_display else "#607261"
    line = "#3b4d3b" if dark_display else "#d5e1d2"
    paper = "#101710" if dark_display else "#f2f7f0"
    panel = "#182219" if dark_display else "#fbfdf9"
    navy = "#dcebd9" if dark_display else "#203c26"
    teal = "#6dbb86" if dark_display else "#357a4a"
    sidebar_text = "#ffffff" if dark_display else "#10150f"
    sidebar_control = "#53663e" if dark_display else "#dce8d5"
    button_text = "#071108" if dark_display else "#ffffff"
    layout = get_setting("dashboard_layout", "Wide")
    css = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
        :root { --ink:__INK__; --muted:__MUTED__; --line:__LINE__; --paper:__PAPER__; --panel:__PANEL__; --navy:__NAVY__; --teal:__TEAL__; }
        html, body, [class*="css"], button, input, textarea, select { font-family:'DM Sans', sans-serif !important; color:var(--ink); }
        [data-testid="stAppViewContainer"] *, [data-testid="stSidebar"] *, [data-testid="stHeader"] * { font-family:'DM Sans', sans-serif !important; }
        [data-testid="stIconMaterial"] { font-family:'Material Symbols Rounded' !important; font-weight:400 !important; }
        .stApp [data-testid="stSidebar"] a, .stApp [data-testid="stSidebar"] p, .stApp [data-testid="stSidebar"] span, .stApp [data-testid="stSidebar"] button { font-family:'DM Sans', sans-serif !important; }
        .stApp { background:var(--paper); color:var(--ink); }
        [data-testid="stMainBlockContainer"] { max-width:__CONTENT_WIDTH__; margin-left:auto; margin-right:auto; }
        [data-testid="stAppViewContainer"], [data-testid="stMain"] { background:var(--paper); color:var(--ink); }
        [data-testid="stAppViewContainer"] p, [data-testid="stAppViewContainer"] label, [data-testid="stAppViewContainer"] span, [data-testid="stAppViewContainer"] small { color:var(--ink) !important; }
        [data-testid="stAppViewContainer"] [data-testid="stMetricLabel"], [data-testid="stAppViewContainer"] .page-subtitle { color:var(--muted) !important; }
        [data-testid="stHeader"] { background:var(--paper); }
        [data-testid="stSidebar"] { background:#3f4f2f; border-right:1px solid #596a45; }
        [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span { color:__SIDEBAR_TEXT__ !important; }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color:__SIDEBAR_TEXT__ !important; }
        [data-testid="stSidebar"] a, [data-testid="stSidebar"] a p, [data-testid="stSidebar"] a span { color:__SIDEBAR_TEXT__ !important; font-weight:600; }
        [data-testid="stSidebarNav"] a, [data-testid="stSidebarNav"] a p, [data-testid="stSidebarNav"] a span,
        [data-testid="stSidebarNav"] [role="link"], [data-testid="stSidebarNav"] [role="link"] p { color:__SIDEBAR_TEXT__ !important; font-family:'DM Sans', sans-serif !important; font-weight:600 !important; }
        [data-testid="stSidebarNav"] > div > div > p { color:__SIDEBAR_TEXT__ !important; font-family:'DM Sans', sans-serif !important; font-weight:700 !important; }
        [data-testid="stSidebar"] a:hover { background:#53663e; color:__SIDEBAR_TEXT__ !important; }
        [data-testid="stSidebar"] [data-baseweb="select"] > div { background:__SIDEBAR_CONTROL__; border-color:#9cac8d; }
        [data-testid="stSidebar"] [data-baseweb="select"] *, [data-testid="stSidebar"] [role="combobox"] { color:__SIDEBAR_TEXT__ !important; }
        [data-testid="stSidebar"] input, [data-testid="stSidebar"] input:focus { background:transparent !important; color:__SIDEBAR_TEXT__ !important; caret-color:__SIDEBAR_TEXT__ !important; font-family:'DM Sans', sans-serif !important; }
        [data-testid="stSidebar"] input::placeholder { color:__SIDEBAR_TEXT__ !important; opacity:.8 !important; }
        [data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"], [data-testid="stSidebarCollapsedControl"] [data-testid="stIconMaterial"] { position:relative; display:inline-block; width:1.5rem; height:1.5rem; font-size:0 !important; color:transparent !important; font-family:'DM Sans', sans-serif !important; }
        [data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"]::before, [data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"]::after, [data-testid="stSidebarCollapsedControl"] [data-testid="stIconMaterial"]::before, [data-testid="stSidebarCollapsedControl"] [data-testid="stIconMaterial"]::after { content:''; position:absolute; top:.5rem; width:.55rem; height:.55rem; border-left:2px solid __SIDEBAR_TEXT__; border-bottom:2px solid __SIDEBAR_TEXT__; transform:rotate(45deg); }
        [data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"]::before, [data-testid="stSidebarCollapsedControl"] [data-testid="stIconMaterial"]::before { left:.35rem; }
        [data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"]::after, [data-testid="stSidebarCollapsedControl"] [data-testid="stIconMaterial"]::after { left:.72rem; }
        [data-testid="stNavSectionHeader"] [data-testid="stIconMaterial"] { position:relative; display:inline-block; width:1rem; height:1rem; font-size:0 !important; color:transparent !important; font-family:'DM Sans', sans-serif !important; text-indent:-9999px; overflow:hidden; }
        [data-testid="stNavSectionHeader"] [data-testid="stIconMaterial"]::before { content:''; position:absolute; top:.25rem; left:.2rem; width:.5rem; height:.5rem; border-right:2px solid __SIDEBAR_TEXT__; border-bottom:2px solid __SIDEBAR_TEXT__; transform:rotate(45deg); }
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button[data-testid="stBaseButton-headerNoPadding"], section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button[data-testid="stBaseButton-headerNoPadding"]:hover { background:transparent !important; background-color:transparent !important; background-image:none !important; border:0 !important; box-shadow:none !important; color:__SIDEBAR_TEXT__ !important; padding:.4rem !important; }
        [data-testid="stSidebarCollapseButton"], [data-testid="stSidebarCollapseButton"] > *, [data-testid="stSidebarCollapseButton"] button > * { background:transparent !important; background-image:none !important; border:0 !important; box-shadow:none !important; }
        [data-testid="stSidebarCollapsedControl"], [data-testid="stSidebarCollapsedControl"] > *, [data-testid="stSidebarCollapsedControl"] button, [data-testid="stSidebarCollapsedControl"] button > * { background:transparent !important; background-image:none !important; border:0 !important; box-shadow:none !important; color:__SIDEBAR_TEXT__ !important; }
        [data-testid="stSidebarCollapseButton"] button:hover { background:#53663e !important; background-color:#53663e !important; border:0 !important; box-shadow:none !important; }
        h1, h2, h3, h1 span, h2 span, h3 span, [data-testid="stHeading"] * { font-family:'DM Sans', sans-serif !important; letter-spacing:0; color:var(--navy) !important; opacity:1 !important; }
        .stApp h1, .stApp h1 span, .stApp h2, .stApp h2 span, .stApp h3, .stApp h3 span { font-family:'DM Sans', sans-serif !important; color:var(--navy) !important; opacity:1 !important; }
        h1 { font-size:2.25rem; margin-bottom:.25rem; }
        h2 { font-size:1.35rem; margin-top:1.5rem; }
        h3 { font-size:1rem; }
        .eyebrow { color:var(--teal); font-size:.72rem; font-weight:700; letter-spacing:.11em; text-transform:uppercase; margin:1rem 0 .35rem; }
        .page-subtitle { color:var(--muted); font-size:1rem; margin:0 0 1.4rem; }
        .section-rule { border-top:1px solid var(--line); margin:1.7rem 0 1.1rem; }
        [data-testid="stMetric"] { background:var(--panel); border:1px solid var(--line); border-radius:6px; padding:1rem 1.1rem; box-shadow:0 2px 8px rgba(23,60,30,.06); }
        [data-testid="stMetricLabel"] { color:var(--muted); }
        [data-testid="stMetricValue"] { color:var(--navy); font-family:'DM Sans', sans-serif; }
        .stButton > button, .stDownloadButton > button, [data-testid^="stBaseButton-"] { background:var(--panel) !important; color:var(--ink) !important; border:1px solid var(--line) !important; border-radius:5px; font-family:'DM Sans', sans-serif !important; font-weight:600; }
        .stButton > button:hover, .stDownloadButton > button:hover, [data-testid^="stBaseButton-"]:hover { background:var(--line) !important; border-color:var(--teal) !important; color:var(--ink) !important; }
        .stButton > button[kind="primary"], [data-testid="stBaseButton-primary"] { background:var(--teal) !important; border-color:var(--teal) !important; color:__BUTTON_TEXT__ !important; }
        .stButton > button[kind="primary"] *, [data-testid="stBaseButton-primary"] * { color:__BUTTON_TEXT__ !important; }
        [data-testid="stDataFrame"] { border:1px solid var(--line); }
        [data-testid="stTextInput"] input, [data-testid="stNumberInput"] input, [data-baseweb="select"] > div, [role="combobox"] { background:var(--panel) !important; color:var(--ink) !important; border:1px solid var(--line); border-radius:5px; font-family:'DM Sans', sans-serif !important; }
        [data-testid="stAppViewContainer"] input[role="combobox"] { color:var(--ink) !important; caret-color:var(--ink) !important; }
        [data-testid="stAppViewContainer"] input::placeholder { color:var(--muted) !important; }
        [data-baseweb="select"] > div:hover, [data-baseweb="select"] > div:focus-within { border-color:var(--teal); box-shadow:0 0 0 1px var(--teal); }
        [role="listbox"], [data-baseweb="popover"] [data-baseweb="menu"] { background:var(--panel); border:1px solid var(--line); color:var(--ink); box-shadow:0 8px 24px rgba(20,45,25,.16); }
        [role="option"], [data-baseweb="menu"] li { color:var(--ink) !important; background:var(--panel); font-family:'DM Sans', sans-serif !important; }
        [role="option"]:hover, [data-baseweb="menu"] li:hover { color:var(--ink) !important; background:var(--line); }
        [aria-selected="true"] { color:var(--ink) !important; background:var(--line); }
        .stAlert { border-radius:4px; }
        </style>
        """
    content_width = "100%" if layout == "Wide" else "min(100%, 960px)"
    st.markdown(css.replace("__INK__", ink).replace("__MUTED__", muted).replace("__LINE__", line).replace("__PAPER__", paper).replace("__PANEL__", panel).replace("__NAVY__", navy).replace("__TEAL__", teal).replace("__SIDEBAR_TEXT__", sidebar_text).replace("__SIDEBAR_CONTROL__", sidebar_control).replace("__BUTTON_TEXT__", button_text).replace("__CONTENT_WIDTH__", content_width), unsafe_allow_html=True)


def page_header(section: str, title: str, subtitle: str) -> None:
    st.markdown(f'<div class="eyebrow">{section}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<p class="page-subtitle">{subtitle}</p>', unsafe_allow_html=True)


def section(title: str) -> None:
    st.markdown('<div class="section-rule"></div>', unsafe_allow_html=True)
    st.subheader(title)
