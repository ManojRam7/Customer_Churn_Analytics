import pandas as pd

from src.preprocessing import (
    FEATURE_NAME_MAP,
    TARGET_COLUMN,
    build_preprocessor,
    normalize_feature_names,
    split_features_target,
)


def test_normalize_feature_names() -> None:
    frame = pd.DataFrame(
        {
            "Usage Frequency": [5],
            "Support Calls": [1],
            "Total Spend": [200.0],
            "Churn": [1],
        }
    )

    normalized = normalize_feature_names(frame)

    assert "Usage_Frequency" in normalized.columns
    assert "Support_Calls" in normalized.columns
    assert "Total_Spend" in normalized.columns
    assert "Usage Frequency" not in normalized.columns


def test_split_features_target() -> None:
    frame = pd.DataFrame(
        {
            "CustomerID": [1, 2],
            "Gender": ["Male", "Female"],
            "Usage_Frequency": [7, 9],
            TARGET_COLUMN: [0, 1],
        }
    )

    x, y = split_features_target(frame)

    assert TARGET_COLUMN not in x.columns
    assert list(y.values) == [0, 1]


def test_build_preprocessor_outputs_expected_width() -> None:
    frame = pd.DataFrame(
        {
            "CustomerID": [1, 2, 3],
            "Age": [22, 30, 45],
            "Gender": ["Male", "Female", "Female"],
            "Subscription_Type": ["Basic", "Premium", "Standard"],
            "Total_Spend": [300.0, 650.5, 980.2],
        }
    )

    preprocessor = build_preprocessor(frame)
    transformed = preprocessor.fit_transform(frame)

    feature_count = len(preprocessor.get_feature_names_out())
    assert transformed.shape[0] == frame.shape[0]
    assert transformed.shape[1] == feature_count
    assert feature_count >= frame.shape[1]


def test_feature_name_map_is_not_empty() -> None:
    assert FEATURE_NAME_MAP
