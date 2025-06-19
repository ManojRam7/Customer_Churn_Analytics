import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pandas as pd
from src.preprocessing import Preprocessor

def test_preprocessor_fit_transform():
    df = pd.DataFrame({
        "Gender": ["Male", "Female"],
        "Subscription Type": ["Basic", "Premium"],
        "Contract Length": ["12m", "Annual"],
        "CustomerID": [1, 2],
        "Age": [25, 30],
        "Tenure": [12, 24],
        "Usage Frequency": [5, 10],
        "Support Calls": [1, 2],
        "Payment Delay": [0, 1],
        "Total Spend": [100.0, 200.0],
        "Last Interaction": [10, 20]
    })
    print("Original DataFrame:\n", df)
    pre = Preprocessor()
    pre.fit(df)
    transformed = pre.transform(df)
    print("Original DataFrame:\n", transformed)
    assert transformed.shape == df.shape
    assert not transformed.isnull().any().any()
    
    
