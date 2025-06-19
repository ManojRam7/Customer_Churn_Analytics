import pandas as pd
import joblib

# Load preprocessed data
df = pd.read_csv('data/processed/preprocessed_from_script.csv')
data_columns = list(df.drop('Churn', axis=1).columns)

# Load model columns
model_columns = joblib.load('models/model_columns.pkl')

print("Columns in preprocessed_from_script.csv:")
print(data_columns)
print("\nColumns saved with the model:")
print(model_columns)

if data_columns == model_columns:
    print("\n✅ Columns match!")
else:
    print("\n❌ Columns do NOT match!")
    # Show differences
    print("In data but not in model:", set(data_columns) - set(model_columns))
    print("In model but not in data:", set(model_columns) - set(data_columns))