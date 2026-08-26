import pandas as pd
import streamlit as st

from data_loader import clean_text, load_data, require_columns
from model_utils import ModelResult, top_probabilities, train_classifier
from ui import apply_theme

apply_theme()

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Threat Level Prediction",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Incident Threat Level")
st.caption("CatBoost context-only estimate: fatalities and injuries are excluded to prevent target leakage.")

# -------------------------------
# Load Dataset
# -------------------------------
df = load_data()
features = ["country_txt", "region_txt", "attacktype1_txt", "weaptype1_txt", "targtype1_txt"]
require_columns(df, features + ["nkill", "nwound"])
df = clean_text(df, features)

# -------------------------------
# Create Threat Level
# -------------------------------
df["impact"] = df["nkill"] + df["nwound"]

def classify_threat(x):
    if x <= 2:
        return "LOW"
    elif x <= 10:
        return "MEDIUM"
    else:
        return "HIGH"

df["threat_level"] = df["impact"].apply(classify_threat)

@st.cache_resource(show_spinner="Training threat model...")
def get_model(frame: pd.DataFrame) -> ModelResult:
    return train_classifier(frame, features, "threat_level")

result = get_model(df)

# -------------------------------
# Sidebar Inputs
# -------------------------------
st.sidebar.header("Input Parameters")

country = st.sidebar.selectbox("Country", sorted(df["country_txt"].unique()))
region = st.sidebar.selectbox("Region", sorted(df["region_txt"].unique()))
attack = st.sidebar.selectbox("Attack Type", sorted(df["attacktype1_txt"].unique()))
weapon = st.sidebar.selectbox("Weapon Type", sorted(df["weaptype1_txt"].unique()))
target = st.sidebar.selectbox("Target Type", sorted(df["targtype1_txt"].unique()))

st.subheader("Model evaluation")
st.info(f"Active model: {result.model_name}")
metric1, metric2 = st.columns(2)
metric1.metric("Macro F1-score", f"{result.macro_f1:.3f}")
metric2.metric("Accuracy", f"{result.accuracy:.3f}")
st.dataframe(pd.DataFrame(result.matrix, index=result.labels, columns=result.labels), use_container_width=True)

# -------------------------------
# Prediction Button
# -------------------------------
if st.button("🚨 Predict Threat Level"):

    input_data = pd.DataFrame([{
        "country_txt": country, "region_txt": region, "attacktype1_txt": attack,
        "weaptype1_txt": weapon, "targtype1_txt": target,
    }])
    prediction = result.pipeline.predict(input_data)[0]

    # -------------------------------
    # Output
    # -------------------------------
    st.subheader("🔍 Prediction Result")

    if prediction == "LOW":
        st.success(f"🟢 Threat Level: {prediction}")
    elif prediction == "MEDIUM":
        st.warning(f"🟡 Threat Level: {prediction}")
    else:
        st.error(f"🔴 Threat Level: {prediction}")
    probabilities = top_probabilities(result, input_data).assign(
        Probability=lambda values: values["Probability"] * 100
    )
    st.dataframe(probabilities.style.format({"Probability": "{:.2f}%"}), use_container_width=True, hide_index=True)