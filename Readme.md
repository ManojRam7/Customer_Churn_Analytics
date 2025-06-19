# Customer Churn Prediction API

A production-ready machine learning pipeline and FastAPI service for predicting customer churn.  
Supports batch predictions, robust preprocessing, and is ready for deployment.

---

## 🚀 Features

- End-to-end pipeline: data cleaning, preprocessing, model training, and inference
- Batch and single-customer predictions via FastAPI
- Health and model info endpoints
- Robust error handling
- Easily deployable (Docker/Azure)

---

## 📁 Project Structure

```
CustomerChurn_Prediction/
│
├── app.py                  # FastAPI app
├── src/
│   ├── preprocessing.py    # Preprocessing logic
│   ├── test.py             # Local batch inference test
│   └── train_model.py      # Model training script
├── models/
│   ├── preprocessor.pkl    # Saved preprocessor
│   ├── random_forest_churn.pkl  # Trained model
│   └── model_columns.pkl   # Model feature columns
├── data/
│   └── processed/
│       ├── eda_cleaned.csv
│       └── preprocessed_from_script.csv
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

1. **Clone the repo and install dependencies:**
    ```bash
    git clone <your-repo-url>
    cd CustomerChurn_Prediction
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. **Preprocess data and train the model:**
    ```bash
    python -m src.preprocessing
    python -m src.train_model
    ```

3. **Run tests (optional):**
    ```bash
    python -m src.test
    ```

4. **Start the FastAPI server:**
    ```bash
    uvicorn app:app --reload --port 8001
    ```

---

## 🛠️ Usage

### **API Endpoints**

#### **1. Health Check**
```http
GET /health
```
**Response:**  
```json
{"status": "ok"}
```

#### **2. Model Info**
```http
GET /model_info
```
**Response:**  
```json
{"model": "RandomForest", "version": "1.0"}
```

#### **3. Predict Churn**
```http
POST /predict
```
**Request Body Example:**
```json
{
  "data": [
    [2.0, 30.0, "Female", 39.0, 14.0, 5.0, 18.0, "Standard", "Annual", 932.0, 17.0],
    [1001, 35, "Male", 12, 5, 1, 0, "Basic", "12m", 500, 30]
  ]
}
```
**Order of fields:**
```
['CustomerID', 'Age', 'Gender', 'Tenure', 'Usage Frequency', 'Support Calls', 'Payment Delay', 'Subscription Type', 'Contract Length', 'Total Spend', 'Last Interaction']
```

**Response Example:**
```json
{
  "predictions": [1.0, 0.0]
}
```

#### **4. Reload Model**
```http
POST /reload_model
```
**Response:**  
```json
{"status": "model reloaded"}
```

---

## 📝 Notes

- Ensure your input data matches the expected column order and types.
- For batch predictions, send multiple rows in the `"data"` array.
- Update model and preprocessor files together after retraining.

---

## ☁️ Deployment

- Ready for Docker and Azure App Service/Container Apps.
- See [FastAPI deployment docs](https://fastapi.tiangolo.com/deployment/) and [Azure Python quickstart](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python).

---

## 📧 Support

For questions or issues, open an issue or contact the