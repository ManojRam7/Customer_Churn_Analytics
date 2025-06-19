import pandas as pd

# Load EDA-cleaned data
df = pd.read_csv('data/processed/eda_cleaned.csv')

# Remove the target column if present
if 'Churn' in df.columns:
    df = df.drop('Churn', axis=1)

# Take the first 3 rows as sample new customers (or use .head(1) for just one)
sample = df.head(3)

# Optionally, modify values to simulate new customers
# For example, sample.iloc[0, :] = [your values here]

# Save as new_customers.csv
#sample.to_csv('data/new_data/new_customers.csv', index=False)
#print("Sample new_customers.csv generated!")


# Save as new customer data
df.to_csv('data/new_data/new_customer_data.csv', index=False)
print("Copied and saved as data/new_data/new_customer_data.csv")