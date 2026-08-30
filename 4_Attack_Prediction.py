import streamlit as st
import pandas as pd

from data_loader import clean_text, load_data, require_columns
from model_utils import ModelResult, top_probabilities, train_classifier
from ui import apply_theme, get_setting, get_setting_bool

apply_theme()

selected_model = get_setting("prediction_model", "CatBoost")

st.set_page_config(
    page_title="Attack Prediction",
    page_icon="✦",
    layout="wide"
)

st.title("✦ Attack Type Prediction")

st.caption(f"{selected_model} classification with native categorical handling, missing-value support, and ranked probabilities.")

# -------------------------
# Load Dataset
# -------------------------

df = load_data()
features = ["country_txt", "region_txt", "weaptype1_txt", "targtype1_txt", "gname", "success", "suicide", "nkill", "nwound", "iyear", "imonth"]
require_columns(df, features + ["attacktype1_txt"])
df = clean_text(df, features[:5])

# -------------------------
# Remove Missing Values
# -------------------------

@st.cache_resource(show_spinner=f"Training {selected_model} attack-type model...")
def get_model(frame: pd.DataFrame, model_name: str) -> ModelResult:
    return train_classifier(frame, features, "attacktype1_txt", model_name=model_name)

result = get_model(df, selected_model)

# -------------------------
# Create Input Form
# -------------------------

with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    with col1:

        country = st.selectbox(
            "Country",
            sorted(df["country_txt"].unique())
        )

        region = st.selectbox(
            "Region",
            sorted(df["region_txt"].unique())
        )

        weapon = st.selectbox(
            "Weapon Type",
            sorted(df["weaptype1_txt"].unique())
        )

        target = st.selectbox(
            "Target Type",
            sorted(df["targtype1_txt"].unique())
        )

    with col2:

        group = st.selectbox(
            "Terrorist Group",
            sorted(df["gname"].unique())
        )

        success = st.selectbox(
            "Attack Successful?",
            [0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

        suicide = st.selectbox(
            "Suicide Attack?",
            [0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

        nkill = st.number_input(
            "Number of Fatalities",
            min_value=0,
            value=0,
            step=1
        )

        nwound = st.number_input(
            "Number of Injured",
            min_value=0,
            value=0,
            step=1
        )

    submitted = st.form_submit_button("Predict Attack Type")
    if submitted:
        st.success("Prediction request received.")

input_df = pd.DataFrame({
    "country_txt": [country],
    "region_txt": [region],
    "weaptype1_txt": [weapon],
    "targtype1_txt": [target],
    "gname": [group],
    "success": [success],
    "suicide": [suicide],
    "nkill": [nkill],
    "nwound": [nwound]
    ,"iyear": [int(df["iyear"].median())], "imonth": [int(df["imonth"].median())]
})

st.subheader("Model evaluation")
st.info(f"Active model: {result.model_name}")
metric1, metric2 = st.columns(2)
metric1.metric("Macro F1-score", f"{result.macro_f1:.3f}")
metric2.metric("Accuracy", f"{result.accuracy:.3f}")
st.metric("Top-3 prediction coverage", f"{result.top3_accuracy:.2%}")
st.dataframe(pd.DataFrame(result.matrix, index=result.labels, columns=result.labels), use_container_width=True)

if get_setting_bool("show_feature_importance", True) and result.feature_importance is not None:
    st.subheader("Feature importance")
    st.bar_chart(result.feature_importance.set_index("Feature")["Importance"].head(10))

if submitted:
    predicted_label = result.pipeline.predict(input_df)[0]
    probabilities = top_probabilities(result, input_df).assign(
        Probability=lambda values: values["Probability"] * 100
    )
    max_probability = float(probabilities["Probability"].max() / 100)
    confidence_threshold = float(get_setting("minimum_prediction_confidence", 80)) / 100
    if max_probability < confidence_threshold:
        st.warning(
            f"Prediction confidence is below the configured threshold ({confidence_threshold * 100:.0f}%). "
            f"The top class is {probabilities.iloc[0]['Prediction']} at {probabilities.iloc[0]['Probability']:.2f}% ."
        )
    st.success(f"Predicted attack type: {predicted_label}")
    if get_setting_bool("show_prediction_probability", True):
        st.dataframe(probabilities.style.format({"Probability": "{:.2f}%"}), use_container_width=True, hide_index=True)

