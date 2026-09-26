# Customer Churn Analytics

Predicts whether a telecom customer will churn from their profile and usage: age, tenure, usage
frequency, support calls, payment delay, subscription type, contract length, total spend and days
since last interaction. A random forest is served by a FastAPI app with a web form for single
customers and a JSON endpoint for batches, packaged in Docker and deployed to Azure.

**Live app:** https://telecomchurnazurewebapp-bjb4f4drcqewc5e2.canadacentral-01.azurewebsites.net

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6-F7931E?logo=scikitlearn&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-0078D4?logo=microsoftazure&logoColor=white)

## Data and results

Kaggle customer churn dataset: 440,833 training rows and 64,374 held-back test rows, 11 features,
57% churners in training.

From `notebooks/Model_training.ipynb` (80/20 split of the training file):

| Model | Accuracy | ROC AUC |
|---|---|---|
| Logistic regression (baseline) | 0.98 | 0.994 |
| Random forest | 1.00 | 1.000 |
| Random forest, 5-fold cross-validation | | 0.991 |
| XGBoost | 1.00 | 1.000 |
| SVM | 0.99 | 1.000 |

The classes in this dataset separate very cleanly, so tree models sit close to the ceiling; the
cross-validated score is the more cautious figure, and `data/raw/test.csv` is kept aside for
checking behaviour on unseen customers. The random forest was kept for serving because it matched the boosted models and
needs no extra dependencies.

## How it is built

1. **EDA** (`notebooks/EDA Analysis.ipynb`, `reports/eda_profile.html`): univariate and
   bivariate analysis, correlations and a full ydata-profiling report.
2. **Preprocessing** (`notebooks/Pre-Processing.ipynb`, `src/preprocessing.py`): encoding of
   gender, subscription and contract, scaling, outlier and correlation checks; SHAP values for
   the random forest are in the training notebook.
3. **Training** (`src/model.py`): a scikit-learn pipeline (preprocessor + random forest with 400
   trees and balanced class weights), 5-fold ROC AUC on the training split, then hold-out metrics.
   Running it writes the model files to `models/` and the metrics to `reports/training_metrics.json`.
4. **Serving** (`app.py`): FastAPI with Pydantic validation of every field, an HTML form at `/`,
   `POST /predict` for batches, `/health` and `/model_info`.
5. **Delivery**: a Docker image; GitHub Actions lints with ruff, runs the tests with coverage and
   builds the image on every push.

## API

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [{"CustomerID": 2, "Age": 30, "Gender": "Female", "Tenure": 39,
                 "Usage_Frequency": 14, "Support_Calls": 5, "Payment_Delay": 18,
                 "Subscription_Type": "Standard", "Contract_Length": "Annual",
                 "Total_Spend": 932.0, "Last_Interaction": 17}]}'
```

```json
{"predictions": [1], "probabilities": [0.8421]}
```

## Run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python -m src.model                       # retrain (optional; trained models are in models/)
uvicorn app:app --reload --port 8080      # http://localhost:8080
pytest --cov=app --cov=src                # tests

docker build -t customer-churn-api .
docker run -p 8080:8080 customer-churn-api
```

## Deploying to Azure

The image is pushed to a registry and the Azure app is pointed at the new tag:

```bash
docker buildx build --platform linux/amd64 -t <registry>/customer-churn-api:<tag> --push .
az containerapp update --name <app> --resource-group <rg> --image <registry>/customer-churn-api:<tag>
```

## Project structure

```text
app.py                      FastAPI app: web form, /predict, /health, /model_info
src/preprocessing.py        feature preparation
src/model.py                training and evaluation
models/                     trained preprocessor, random forest, XGBoost model, column list
templates/index.html        web form
notebooks/                  EDA, preprocessing, model training and comparison
data/raw/                   train.csv, test.csv
reports/eda_profile.html    profiling report
tests/                      API and preprocessing tests
Dockerfile, .github/workflows/ci.yml
```
