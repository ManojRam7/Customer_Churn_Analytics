import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib


class Preprocessor:
    def __init__(self):
        self.cat_cols = None
        self.num_cols = None
        self.label_encoders = {}
        self.scaler = None

    def fit(self, df):
        # Identify categorical and numerical columns
        self.cat_cols = df.select_dtypes(include='object').columns.tolist()
        self.num_cols = df.select_dtypes(include=np.number).columns.drop('Churn', errors='ignore').tolist()

        # Fit label encoders for categorical columns
        for col in self.cat_cols:
            le = LabelEncoder()
            df[col] = df[col].astype(str)
            le.fit(df[col])
            self.label_encoders[col] = le

        # Fit scaler for numerical columns
        self.scaler = StandardScaler()
        self.scaler.fit(df[self.num_cols])

    def transform(self, df):
        df = df.copy()

        # Encode categorical columns
        for col in self.cat_cols:
            le = self.label_encoders.get(col)
            if le:
                df[col] = df[col].astype(str)
                # Handle unseen labels
                df[col] = df[col].map(lambda s: s if s in le.classes_ else 'unknown')
                if 'unknown' not in le.classes_:
                    le.classes_ = np.append(le.classes_, 'unknown')
                df[col] = le.transform(df[col])
            else:
                df[col] = 0  # or np.nan

        # Scale numerical columns
        df[self.num_cols] = self.scaler.transform(df[self.num_cols])

        return df

    def fit_transform(self, df):
        self.fit(df)
        return self.transform(df)


# Example usage for training:
if __name__ == "__main__":
    # Use EDA-cleaned data for fitting the preprocessor
    df = pd.read_csv('data/processed/eda_cleaned.csv')
    preprocessor = Preprocessor()
    df_processed = preprocessor.fit_transform(df)

    # Save the preprocessor for later use (for inference/deployment)
    joblib.dump(preprocessor, 'models/preprocessor.pkl')

    # Optionally, save the processed data
    df_processed.to_csv(
        'data/processed/preprocessed_from_script.csv', index=False
    )