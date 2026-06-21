# Customer Churn Prediction API 🚀

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6-orange.svg)](https://scikit-learn.org/)
[![CI](https://img.shields.io/github/actions/workflow/status/ManojRam7/CustomerChurn_Prediction/ci.yml?branch=main&label=CI)](https://github.com/ManojRam7/CustomerChurn_Prediction/actions)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

Production-focused machine learning service for telecom churn prediction, built with a modern Python stack and portfolio-ready project hygiene.

## Highlights ✨

- Typed and validated FastAPI API for single/batch churn scoring.
- Web UI for interactive inference with probability output.
- Reproducible ML training pipeline with cross-validation metrics.
- CI workflow for linting, testing, and Docker build verification.
- Cloud-vendor-neutral setup with no Azure-specific dependency.

## Project Structure 🧭

```text
CustomerChurn_Prediction/
├── app.py                         # FastAPI app + HTML routes
├── requirements.txt               # Runtime + dev dependencies
├── Dockerfile                     # Containerized deployment
├── data/
│   ├── raw/                       # Original datasets
│   ├── processed/                 # Processed datasets
│   └── new_data/                  # New inference examples
├── models/                        # Serialized model artifacts
├── reports/                       # Metrics and EDA reports
├── src/
│   ├── preprocessing.py           # Feature normalization + preprocessing
│   └── model.py                   # Training + evaluation pipeline
├── templates/
│   └── index.html                 # Responsive UI for inference
└── tests/
    ├── test_api.py
    └── test_preprocessing.py
```

## Quickstart ⚡

### 1) Create and activate environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Run API locally

```bash
uvicorn app:app --reload --port 8080
```

Open http://localhost:8080

### 4) Run tests

```bash
pytest --cov=app --cov=src --cov-report=term-missing
```

## API Usage 🧪

### Predict endpoint

- Method: POST
- URL: /predict
- Body:

```json
{
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
}
```

Expected response:

```json
{
  "predictions": [1],
  "probabilities": [0.8421]
}
```

## Train / Retrain Model 🧠

```bash
python -m src.model
```

Outputs:

- models/preprocessor.pkl
- models/random_forest_churn_from_script.pkl
- models/model_columns.pkl
- reports/training_metrics.json

## Docker 🐳

```bash
docker build -t customer-churn-api:latest .
docker run -p 8080:8080 customer-churn-api:latest
```

## Portfolio Notes 📌

This project demonstrates:

- End-to-end ML service delivery (data -> model -> API -> UI -> CI)
- Practical production engineering conventions in data science projects
- Reusable and testable components for future MLOps extension

## License 📄

This project is provided for educational and portfolio use.
