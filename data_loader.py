from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PATH = PROJECT_ROOT / "data" / "global_terrorism_db.csv"


@st.cache_data(show_spinner="Loading GTD dataset...")
def load_data(path: str | None = None) -> pd.DataFrame:
    """Load and lightly normalize the GTD dataset from one consistent path."""
    dataset_path = Path(path) if path else DATA_PATH
    if not dataset_path.exists():
        raise FileNotFoundError(
            f"GTD dataset not found at {dataset_path}. "
            "Place global_terrorism_db.csv in the data folder."
        )

    df = pd.read_csv(dataset_path, encoding="latin1", low_memory=False)
    numeric_columns = [
        "iyear", "imonth", "iday", "latitude", "longitude", "nkill", "nwound",
        "success", "suicide",
    ]
    for column in numeric_columns:
        if column in df:
            df[column] = pd.to_numeric(df[column], errors="coerce")
    for column in ("nkill", "nwound"):
        if column in df:
            df[column] = df[column].fillna(0)
    return df


def require_columns(df: pd.DataFrame, columns: list[str]) -> None:
    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(missing)}")


def clean_text(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Fill categorical gaps without discarding otherwise useful incidents."""
    result = df.copy()
    for column in columns:
        if column in result:
            result[column] = result[column].fillna("Unknown").astype(str)
    return result