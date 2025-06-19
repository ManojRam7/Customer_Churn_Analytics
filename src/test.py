import pandas as pd
import joblib

#from preprocessing import Preprocessor
from src.preprocessing import Preprocessor
import joblib

preprocessor = joblib.load('models/preprocessor.pkl')


# Load preprocessor and model
preprocessor = joblib.load('models/preprocessor.pkl')

model = joblib.load('models/random_forest_churn_from_script.pkl') 

# Load new data (should have the same columns as training data before preprocessing)
new_data = pd.read_csv('/Users/manojrammopati/Projects/ds_template/CustomerChurn_Prediction/data/new_data/new_customer_data.csv')

# Preprocess new data
new_data_processed = preprocessor.transform(new_data)

# After preprocessing new data
new_data_processed = preprocessor.transform(new_data)

# Save the columns used for the model
joblib.dump(list(new_data_processed.columns), 'models/model_columns.pkl')

# Predict
predictions = model.predict(new_data_processed)
print("Predicted churn for new batch", predictions)

