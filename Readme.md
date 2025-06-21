# Customer Churn Prediction Website

A robust, production-ready machine learning web service for telecom customer churn prediction.  
Built with **FastAPI**, **Docker**, and **Azure Container Apps**.  
Automated CI/CD with **GitHub Actions** and **Docker Hub**.

---

## 🚀 Features

- **Data Analysis**:data cleaning, preprocessing, model training, and inference testing
- **Machine Learning Model**: Powered by a trained Random Forest model.
- **FASTAPI BACK-END-POINT**: Batch and single-customer predictions via FastAPI API.
- **POSTMAN**: Batch and single-customer predictions via `/predict` endpoint.
- **FRONT-END-POINT WEB UI**: Responsive, user-friendly HTML form with live predictions.
- **Automated CI/CD**: Every push is tested, containerized to Docker Hub, and deployed to Azure Conatiner APP.
- **DOCKER IMAGE**: Docker image generated and extracted to Docker Desktop and Pushed to Docker HUb.
- **AZURE Cloud**: Runs on scalable, Health and model info endpoints,secure Azure Container Apps.
- **Secrets Management**: All credentials handled securely via GitHub Secrets.

---

## 📁 Project Structure

```
CustomerChurn_Prediction/
│
├── app.py                  # FastAPI app (API + HTML frontend)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker build instructions
├── models/
│   ├── preprocessor.pkl    # Saved preprocessor
│   ├── random_forest_churn_from_script.pkl  # Trained model
│   └── model_columns.pkl   # Model feature columns
├── templates/
│   └── index.html          # Jinja2 HTML template for the web form
├── src/                    # (Optional) Scripts for training, preprocessing, testing
│   ├── preprocessing.py
│   ├── train_model.py
│   └── test.py
├── data/                   # (Optional) Data files
│   └── processed/
│       ├── eda_cleaned.csv
│       └── preprocessed_from_script.csv
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

2. **Preprocess data and train the model (if needed):**
    ```bash
    python src/preprocessing.py
    python src/train_model.py
    ```

3. **Run tests (optional):**
    ```bash
    python src/test.py
    ```

4. **Start the FastAPI server (with HTML frontend):**
    ```bash
    uvicorn app:app --reload --port 8080
    ```
    - Visit [http://localhost:8080](http://localhost:8080) for the web form.
    - Use `/predict` endpoint for API predictions.

---

## 🛠️ Usage

### **A. Web Frontend**

- Open [http://localhost:8080](http://localhost:8080) in your browser.
- Fill in the form and click **Predict Churn** to see results.
- Use the **Clear** button to reset the form.

### **B. API Endpoints**

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
Content-Type: application/json
```
**Request Body Example:**
```json
{
  "data": [
    {
      "CustomerID": 1,
      "Age": 35,
      "Gender": "Male",
      "Tenure": 12,
      "Usage_Frequency": 5,
      "Support_Calls": 2,
      "Payment_Delay": 0,
      "Subscription_Type": "Standard",
      "Contract_Length": "Annual",
      "Total_Spend": 1200,
      "Last_Interaction": 5
    }
  ]
}
```
**Response Example:**
```json
{
  "predictions": [0]
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

- Ensure your input data matches the expected column names and types.
- For batch predictions, send multiple objects in the `"data"` array.
- Update model and preprocessor files together after retraining.
- The HTML form retains values after prediction and features a clear button and watermark.

---

## 🐳 Dockerization

1. **Build the Docker image for amd64 (required for Azure):**
    ```bash
    docker build --platform linux/amd64 -t manojram7/customer-churn-api:latest .
    ```

2. **Run locally:**
    ```bash
    docker run -p 8080:8080 manojram7/customer-churn-api:latest
    ```

3. **Push to Docker Hub:**
    ```bash
    docker push manojram7/customer-churn-api:latest
    ```

---

## ☁️ Azure Container App Deployment

1. **Create a Container App in Azure Portal:**
    - **Image source:** Docker Hub
    - **Registry login server:** `docker.io`
    - **Image and tag:** `manojram7/customer-churn-api:latest`
    - **Target port:** `8080`
    - **Ingress:** Enabled (public access if needed)

2. **After deployment, access your app at the provided Azure URL.**

3. **Test the `/` (web form) and `/predict` (API) endpoints.**

---

## 📧 Support

For questions or issues, open an issue or contact the maintainer.

---

**Happy Predicting!**