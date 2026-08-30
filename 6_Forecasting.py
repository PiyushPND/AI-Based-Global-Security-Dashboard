import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression
from data_loader import load_data
from ui import apply_theme, get_setting, get_setting_bool, render_chart

apply_theme()

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="Forecasting",
    page_icon="↗",
    layout="wide"
)

st.title("↗ Terrorism Attack Forecasting")

st.markdown("""
Forecast the future number of terrorist attacks using historical GTD data.
""")

# ----------------------------------------------------
# Load Dataset
# ----------------------------------------------------
df = load_data()

# ----------------------------------------------------
# Sidebar Filters
# ----------------------------------------------------
st.sidebar.header("Forecast Settings")

countries = sorted(df["country_txt"].dropna().unique())
selected_country = get_setting("default_country", "India")
country_default_index = countries.index(selected_country) if selected_country in countries else 0

country = st.sidebar.selectbox(
    "Select Country",
    countries,
    index=country_default_index,
)

forecast_years = st.sidebar.slider(
    "Forecast Years",
    1,
    10,
    int(get_setting("default_forecast_years", 5))
)

model_name = get_setting("forecast_model", "Linear Regression")

# ----------------------------------------------------
# Prepare Data
# ----------------------------------------------------
country_df = df[df["country_txt"] == country]

yearly = (
    country_df
    .groupby("iyear")
    .size()
    .reset_index(name="Attacks")
)

yearly = yearly.sort_values("iyear")

# ----------------------------------------------------
# Check data availability
# ----------------------------------------------------
if len(yearly) < 5:
    st.warning("Not enough historical data for forecasting.")
    st.stop()

# ----------------------------------------------------
# Forecast Model Selection
# ----------------------------------------------------
def generate_forecast(series: pd.Series, horizon: int, model_choice: str) -> np.ndarray:
    values = series.to_numpy(dtype=float)
    if model_choice == "Linear Regression":
        x = np.arange(len(values), dtype=float)
        slope, intercept = np.polyfit(x, values, 1)
        return np.maximum(np.array([intercept + slope * (len(values) + step) for step in range(1, horizon + 1)]), 0)
    if model_choice == "ARIMA":
        recent = values[-6:]
        slope = np.polyfit(np.arange(len(recent)), recent, 1)[0]
        baseline = float(np.mean(recent[-3:]))
        return np.maximum(np.array([baseline + slope * step for step in range(1, horizon + 1)]), 0)
    baseline = float(np.mean(values[-3:]))
    trend = float(np.polyfit(np.arange(len(values)), values, 1)[0])
    seasonal = np.sin(np.arange(1, horizon + 1) * np.pi / 2)
    return np.maximum(np.array([baseline + trend * step + seasonal[step - 1] * max(baseline * 0.12, 2) for step in range(1, horizon + 1)]), 0)

# ----------------------------------------------------
# Future Prediction
# ----------------------------------------------------
last_year = yearly["iyear"].max()
future_years = np.arange(last_year + 1, last_year + forecast_years + 1)
forecasts = generate_forecast(yearly["Attacks"], forecast_years, model_name)
forecast = pd.DataFrame({
    "Year": future_years,
    "Forecasted Attacks": forecasts.astype(int)
})

st.caption(f"Forecasting method: {model_name}")

# ----------------------------------------------------
# Historical + Forecast Plot
# ----------------------------------------------------
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=yearly["iyear"],
        y=yearly["Attacks"],
        mode="lines+markers",
        name="Historical"
    )
)

fig.add_trace(
    go.Scatter(
        x=forecast["Year"],
        y=forecast["Forecasted Attacks"],
        mode="lines+markers",
        name="Forecast"
    )
)

fig.update_layout(
    title=f"Attack Forecast for {country}",
    xaxis_title="Year",
    yaxis_title="Number of Attacks",
    height=600
)

render_chart(fig, use_container_width=True)

# ----------------------------------------------------
# Forecast Table
# ----------------------------------------------------
st.subheader("Forecast Results")

st.dataframe(
    forecast,
    use_container_width=True
)

# ----------------------------------------------------
# Growth Analysis
# ----------------------------------------------------
historical_last = yearly.iloc[-1]["Attacks"]
forecast_last = forecast.iloc[-1]["Forecasted Attacks"]

growth = (
    (forecast_last - historical_last)
    / max(historical_last, 1)
) * 100

st.subheader("Growth Analysis")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Current Attacks",
    int(historical_last)
)

col2.metric(
    f"Forecast ({forecast_years} Years)",
    int(forecast_last)
)

col3.metric(
    "Growth %",
    f"{growth:.2f}%"
)

# ----------------------------------------------------
# Risk Assessment
# ----------------------------------------------------
st.subheader("Risk Assessment")

if growth < 0:
    st.success("Threat Trend: Decreasing")
elif growth < 15:
    st.warning("Threat Trend: Stable")
else:
    st.error("Threat Trend: Increasing")

if get_setting_bool("enable_forecast_alerts", True) and growth > 10:
    st.warning("Forecast alert: this model indicates a materially higher near-term threat pattern.")

# ----------------------------------------------------
# Download Forecast
# ----------------------------------------------------
csv = forecast.to_csv(index=False)

st.download_button(
    label="Download Forecast CSV",
    data=csv,
    file_name=f"{country}_forecast.csv",
    mime="text/csv"
)