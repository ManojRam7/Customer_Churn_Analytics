from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

TARGET_COLUMN = "Churn"

FEATURE_NAME_MAP = {
    "Usage Frequency": "Usage_Frequency",
    "Support Calls": "Support_Calls",
    "Payment Delay": "Payment_Delay",
    "Subscription Type": "Subscription_Type",
    "Contract Length": "Contract_Length",
    "Total Spend": "Total_Spend",
    "Last Interaction": "Last_Interaction",
}


class Preprocessor:
    """Legacy preprocessor kept for backward compatibility with existing pickles."""

    def __init__(self) -> None:
        self.cat_cols: list[str] | None = None
        self.num_cols: list[str] | None = None
        self.label_encoders: dict[str, LabelEncoder] = {}
        self.scaler: StandardScaler | None = None

    def fit(self, df: pd.DataFrame) -> None:
        self.cat_cols = df.select_dtypes(include="object").columns.tolist()
        self.num_cols = (
            df.select_dtypes(include=np.number)
            .columns.drop(TARGET_COLUMN, errors="ignore")
            .tolist()
        )

        for column in self.cat_cols:
            encoder = LabelEncoder()
            series = df[column].astype(str)
            encoder.fit(series)
            self.label_encoders[column] = encoder

        self.scaler = StandardScaler()
        self.scaler.fit(df[self.num_cols])

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.cat_cols is None or self.num_cols is None or self.scaler is None:
            raise ValueError("Preprocessor is not fitted")

        frame = df.copy()

        for column in self.cat_cols:
            encoder = self.label_encoders.get(column)
            if encoder is None:
                frame[column] = 0
                continue

            frame[column] = frame[column].astype(str)
            frame[column] = frame[column].map(
                lambda value: value if value in encoder.classes_ else "unknown"
            )
            if "unknown" not in encoder.classes_:
                encoder.classes_ = np.append(encoder.classes_, "unknown")
            frame[column] = encoder.transform(frame[column])

        frame[self.num_cols] = self.scaler.transform(frame[self.num_cols])
        return frame

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.fit(df)
        return self.transform(df)


def normalize_feature_names(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.rename(columns=FEATURE_NAME_MAP)


def load_training_data(path: Path | None = None) -> pd.DataFrame:
    source_path = path or (DATA_DIR / "raw" / "train.csv")
    data = pd.read_csv(source_path)
    data = normalize_feature_names(data)
    return data


def split_features_target(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    x = frame.drop(columns=[TARGET_COLUMN])
    y = frame[TARGET_COLUMN].astype(int)
    return x, y


def build_preprocessor(features: pd.DataFrame) -> ColumnTransformer:
    categorical_cols = features.select_dtypes(include=["object"]).columns.tolist()
    numeric_cols = [c for c in features.columns if c not in categorical_cols]

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "encoder",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            ),
        ]
    )

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("cat", categorical_transformer, categorical_cols),
            ("num", numeric_transformer, numeric_cols),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )


def fit_and_save_preprocessor() -> None:
    frame = load_training_data()
    x_train, _ = split_features_target(frame)
    preprocessor = build_preprocessor(x_train)
    preprocessor.fit(x_train)

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(preprocessor, MODELS_DIR / "preprocessor.pkl")


if __name__ == "__main__":
    fit_and_save_preprocessor()
    print("Preprocessor fitted and saved to models/preprocessor.pkl")
