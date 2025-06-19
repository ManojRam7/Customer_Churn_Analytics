import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

# Load preprocessed data
df = pd.read_csv('data/processed/preprocessed_from_script.csv')

# Separate features and target
X = df.drop('Churn', axis=1)
y = df['Churn']

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Save model
joblib.dump(model, 'models/random_forest_churn_from_script.pkl')

# Optionally, save the column order for inference
joblib.dump(list(X.columns), 'models/model_columns.pkl')

print("Model trained and saved successfully.")