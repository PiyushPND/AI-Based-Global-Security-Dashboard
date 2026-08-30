from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
try:
    from catboost import CatBoostClassifier
except ImportError:
    CatBoostClassifier = None
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier


@dataclass
class ModelResult:
    pipeline: Any
    model_name: str
    labels: list[str]
    macro_f1: float
    accuracy: float
    top3_accuracy: float
    matrix: list[list[int]]
    feature_importance: pd.DataFrame | None = None


def _make_model(model_name: str):
    if model_name == "Random Forest":
        return RandomForestClassifier(
            n_estimators=220, min_samples_leaf=2,
            class_weight="balanced_subsample", random_state=42, n_jobs=-1,
        )
    if model_name == "Decision Tree":
        return DecisionTreeClassifier(
            max_depth=12, min_samples_leaf=3, random_state=42,
            class_weight="balanced"
        )
    if model_name == "Gradient Boosting":
        return GradientBoostingClassifier(random_state=42)
    if CatBoostClassifier is not None:
        return CatBoostClassifier(
            iterations=350, depth=8, learning_rate=0.08,
            loss_function="MultiClass", eval_metric="TotalF1:average=Macro",
            random_seed=42, verbose=False, thread_count=-1,
            allow_writing_files=False,
        )
    return RandomForestClassifier(
        n_estimators=180, min_samples_leaf=2,
        class_weight="balanced_subsample", random_state=42, n_jobs=-1,
    )


def _get_feature_importance(model, feature_names):
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "get_feature_importance"):
        importances = model.get_feature_importance()
    else:
        importances = np.zeros(len(feature_names))
    frame = pd.DataFrame({"Feature": feature_names, "Importance": importances})
    return frame.sort_values("Importance", ascending=False).head(10)


def train_classifier(
    frame: pd.DataFrame,
    features: list[str],
    target: str,
    sample_size: int = 100_000,
    model_name: str | None = None,
) -> ModelResult:
    requested = model_name or ("CatBoost" if CatBoostClassifier is not None else "Random Forest")
    data = frame[features + [target]].copy().dropna(subset=[target])
    if len(data) > sample_size:
        data = data.sample(sample_size, random_state=42)
    data[target] = data[target].astype(str)
    labels = sorted(data[target].unique().tolist())
    if len(labels) < 2:
        raise ValueError(f"{target} needs at least two classes to train a model.")

    X = data[features].copy()
    y = data[target]
    categorical = X.select_dtypes(include=["object", "category"]).columns.tolist()
    if CatBoostClassifier is not None and requested == "CatBoost":
        X[categorical] = X[categorical].fillna("Unknown").astype(str)
        categorical_indices = [X.columns.get_loc(column) for column in categorical]
        model = _make_model(requested)
        model_name = "CatBoost"
    else:
        numeric = [column for column in features if column not in categorical]
        preprocessor = ColumnTransformer([
            ("categorical", Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore")),
            ]), categorical),
            ("numeric", SimpleImputer(strategy="median"), numeric),
        ])
        model = Pipeline([
            ("preprocessor", preprocessor),
            ("model", _make_model(requested)),
        ])
        model_name = requested
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    if CatBoostClassifier is not None and requested == "CatBoost":
        model.fit(X_train, y_train, cat_features=categorical_indices)
        predicted = model.predict(X_test).ravel()
    else:
        model.fit(X_train, y_train)
        predicted = model.predict(X_test)
    probabilities = model.predict_proba(X_test)
    classes = model.classes_ if CatBoostClassifier is not None and requested == "CatBoost" else model.named_steps["model"].classes_
    top_three = classes[probabilities.argsort(axis=1)[:, -3:]]
    feature_names = list(X.columns)
    if isinstance(model, Pipeline):
        fitted_model = model.named_steps["model"]
        feature_names = list(model.named_steps["preprocessor"].get_feature_names_out())
        importances = _get_feature_importance(fitted_model, feature_names)
    elif CatBoostClassifier is not None and requested == "CatBoost":
        importances = _get_feature_importance(model, feature_names)
    else:
        importances = pd.DataFrame({"Feature": feature_names, "Importance": np.zeros(len(feature_names))})
    return ModelResult(
        pipeline=model,
        model_name=model_name,
        labels=labels,
        macro_f1=f1_score(y_test, predicted, average="macro", zero_division=0),
        accuracy=accuracy_score(y_test, predicted),
        top3_accuracy=sum(
            actual in guesses for actual, guesses in zip(y_test, top_three)
        ) / len(y_test),
        matrix=confusion_matrix(y_test, predicted, labels=labels).tolist(),
        feature_importance=importances,
    )


def top_probabilities(result: ModelResult, row: pd.DataFrame, limit: int = 5) -> pd.DataFrame:
    probabilities = result.pipeline.predict_proba(row)[0]
    classes = (
        result.pipeline.classes_
        if hasattr(result.pipeline, "classes_")
        else result.pipeline.named_steps["model"].classes_
    )
    output = pd.DataFrame({"Prediction": classes, "Probability": probabilities})
    return output.sort_values("Probability", ascending=False).head(limit)