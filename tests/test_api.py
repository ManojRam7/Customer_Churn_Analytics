from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_predict_valid():
    response = client.post("/predict", json={
        "data": [
            {
                "CustomerID": 2,
                "Age": 30,
                "Gender": "Female",
                "Tenure": 39,
                "Usage_Frequency": 14,
                "Support_Calls": 5,
                "Payment_Delay": 18,
                "Subscription_Type": "Standard",
                "Contract_Length": "Annual",
                "Total_Spend": 932.0,
                "Last_Interaction": 17
            }
        ]
    })
    print("API response (valid):", response.json())
    assert response.status_code == 200
    assert "predictions" in response.json()
    assert isinstance(response.json()["predictions"], list)

def test_predict_invalid_gender():
    response = client.post("/predict", json={
        "data": [
            {
                "CustomerID": 2,
                "Age": 30,
                "Gender": "Alien",
                "Tenure": 39,
                "Usage_Frequency": 14,
                "Support_Calls": 5,
                "Payment_Delay": 18,
                "Subscription_Type": "Standard",
                "Contract_Length": "Annual",
                "Total_Spend": 932.0,
                "Last_Interaction": 17
            }
        ]
    })
    print("API response (invalid gender):", response.json())
    assert response.status_code == 422

def test_predict_batch():
    response = client.post("/predict", json={
        "data": [
            {
                "CustomerID": 2,
                "Age": 30,
                "Gender": "Female",
                "Tenure": 39,
                "Usage_Frequency": 14,
                "Support_Calls": 5,
                "Payment_Delay": 18,
                "Subscription_Type": "Standard",
                "Contract_Length": "Annual",
                "Total_Spend": 932.0,
                "Last_Interaction": 17
            },
            {
                "CustomerID": 1001,
                "Age": 35,
                "Gender": "Male",
                "Tenure": 12,
                "Usage_Frequency": 5,
                "Support_Calls": 1,
                "Payment_Delay": 0,
                "Subscription_Type": "Basic",
                "Contract_Length": "12m",
                "Total_Spend": 500.0,
                "Last_Interaction": 30
            }
        ]
    })
    print("API response (batch):", response.json())
    assert response.status_code == 200
    assert "predictions" in response.json()
    assert len(response.json()["predictions"]) == 2

def test_predict_invalid_shape():
    response = client.post("/predict", json={
        "data": [
            {
                "CustomerID": 2,
                "Age": 30
                # Missing required fields
            }
        ]
    })
    print("API response (invalid shape):", response.json())
    assert response.status_code == 422










'''

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_predict_valid():
    response = client.post("/predict", json={
        "data": [
            {
                "CustomerID": 2,
                "Age": 30,
                "Gender": "Female",
                "Tenure": 39,
                "Usage_Frequency": 14,
                "Support_Calls": 5,
                "Payment_Delay": 18,
                "Subscription_Type": "Standard",
                "Contract_Length": "Annual",
                "Total_Spend": 932.0,
                "Last_Interaction": 17
            }
        ]
    })
    assert response.status_code == 200
    assert "predictions" in response.json()
    assert isinstance(response.json()["predictions"], list)

def test_predict_invalid_gender():
    response = client.post("/predict", json={
        "data": [
            {
                "CustomerID": 2,
                "Age": 30,
                "Gender": "Alien",
                "Tenure": 39,
                "Usage_Frequency": 14,
                "Support_Calls": 5,
                "Payment_Delay": 18,
                "Subscription_Type": "Standard",
                "Contract_Length": "Annual",
                "Total_Spend": 932.0,
                "Last_Interaction": 17
            }
        ]
    })
    assert response.status_code == 422

def test_predict_batch():
    response = client.post("/predict", json={
        "data": [
            {
                "CustomerID": 2,
                "Age": 30,
                "Gender": "Female",
                "Tenure": 39,
                "Usage_Frequency": 14,
                "Support_Calls": 5,
                "Payment_Delay": 18,
                "Subscription_Type": "Standard",
                "Contract_Length": "Annual",
                "Total_Spend": 932.0,
                "Last_Interaction": 17
            },
            {
                "CustomerID": 1001,
                "Age": 35,
                "Gender": "Male",
                "Tenure": 12,
                "Usage_Frequency": 5,
                "Support_Calls": 1,
                "Payment_Delay": 0,
                "Subscription_Type": "Basic",
                "Contract_Length": "12m",
                "Total_Spend": 500.0,
                "Last_Interaction": 30
            }
        ]
    })
    assert response.status_code == 200
    assert "predictions" in response.json()
    assert len(response.json()["predictions"]) == 2
  
  
  
  
  
    
def test_predict_invalid_shape():
    response = client.post("/predict", json={
        "data": [
            {
                "CustomerID": 2,
                "Age": 30,
            }
        ]
    })    
                
def test_predict_valid():
    response = client.post("/predict", json={
    "data": [
        {
            "CustomerID": 2,
            "Age": 30,
            "Gender": "Female",
            "Tenure": 39,
            "Usage_Frequency": 14,
            "Support_Calls": 5,
            "Payment_Delay": 18,
            "Subscription_Type": "Standard",
            "Contract_Length": "Annual",
            "Total_Spend": 932.0,
            "Last_Interaction": 17
        }
    ]
})
    print("API response from Pytests == ", response.json())
    assert response.status_code == 200                
    
    
'''