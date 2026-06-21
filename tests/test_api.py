from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def _valid_payload() -> dict:
    return {
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
                "Last_Interaction": 17,
            }
        ]
    }


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_valid() -> None:
    response = client.post("/predict", json=_valid_payload())
    body = response.json()

    assert response.status_code == 200
    assert "predictions" in body
    assert isinstance(body["predictions"], list)
    assert len(body["predictions"]) == 1

    if "probabilities" in body:
        assert isinstance(body["probabilities"], list)
        assert 0.0 <= body["probabilities"][0] <= 1.0


def test_predict_invalid_gender() -> None:
    payload = _valid_payload()
    payload["data"][0]["Gender"] = "Alien"

    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_batch() -> None:
    payload = _valid_payload()
    payload["data"].append(
        {
            "CustomerID": 1001,
            "Age": 35,
            "Gender": "Male",
            "Tenure": 12,
            "Usage_Frequency": 5,
            "Support_Calls": 1,
            "Payment_Delay": 0,
            "Subscription_Type": "Basic",
            "Contract_Length": "Quarterly",
            "Total_Spend": 500.0,
            "Last_Interaction": 30,
        }
    )

    response = client.post("/predict", json=payload)
    body = response.json()

    assert response.status_code == 200
    assert "predictions" in body
    assert len(body["predictions"]) == 2


def test_predict_missing_fields() -> None:
    response = client.post("/predict", json={"data": [{"CustomerID": 2, "Age": 30}]})
    assert response.status_code == 422
