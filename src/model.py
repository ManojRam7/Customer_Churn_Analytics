import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline

from src.preprocessing import (
    TARGET_COLUMN,
    build_preprocessor,
    load_training_data,
    split_features_target,
)

BASE_DIR = Path(__file__).resolve().parents[1]
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"


def train_model(random_state: int = 42) -> dict[str, object]:
    frame = load_training_data()
    x, y = split_features_target(frame)

    x_train, x_valid, y_train, y_valid = train_test_split(
        x,
        y,
        test_size=0.2,
        stratify=y,
        random_state=random_state,
    )

    preprocessor = build_preprocessor(x_train)
    classifier = RandomForestClassifier(
        n_estimators=400,
        max_depth=None,
        min_samples_split=4,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=random_state,
        n_jobs=-1,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", classifier),
        ]
    )

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
    cv_auc = cross_val_score(
        pipeline,
        x_train,
        y_train,
        scoring="roc_auc",
        cv=cv,
        n_jobs=-1,
    )

    pipeline.fit(x_train, y_train)

    y_pred = pipeline.predict(x_valid)
    y_proba = pipeline.predict_proba(x_valid)[:, 1]

    report = classification_report(y_valid, y_pred, output_dict=True)
    valid_auc = float(roc_auc_score(y_valid, y_proba))

    metrics = {
        "cv_auc_mean": float(cv_auc.mean()),
        "cv_auc_std": float(cv_auc.std()),
        "valid_auc": valid_auc,
        "precision_class_1": float(report["1"]["precision"]),
        "recall_class_1": float(report["1"]["recall"]),
        "f1_class_1": float(report["1"]["f1-score"]),
    }

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # Save separate assets for compatibility with the FastAPI app.
    fitted_preprocessor = pipeline.named_steps["preprocessor"]
    fitted_model = pipeline.named_steps["model"]

    model_columns = fitted_preprocessor.get_feature_names_out().tolist()

    joblib.dump(fitted_preprocessor, MODELS_DIR / "preprocessor.pkl")
    joblib.dump(fitted_model, MODELS_DIR / "random_forest_churn_from_script.pkl")
    joblib.dump(model_columns, MODELS_DIR / "model_columns.pkl")

    with open(REPORTS_DIR / "training_metrics.json", "w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2)

    return metrics


if __name__ == "__main__":
    summary = train_model()
    print("Training complete")
    print(pd.Series(summary).to_string())
