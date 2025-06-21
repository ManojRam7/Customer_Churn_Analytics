# 📊 Customer Churn Prediction Platform

[![CI/CD](https://github.com/ManojRam7/CustomerChurn_Prediction/actions/workflows/ci.yml/badge.svg)](https://github.com/ManojRam7/CustomerChurn_Prediction/actions)
[![Docker Pulls](https://img.shields.io/docker/pulls/manojram7/customer-churn-api)](https://hub.docker.com/r/manojram7/customer-churn-api)

A robust, production-ready machine learning web service for telecom customer churn prediction.  
Built with **FastAPI**, **Docker**, and **Azure Container Apps**.  
Automated CI/CD with **GitHub Actions** and **Docker Hub**.

---

## 🚀 Features

- **Accurate Churn Prediction**: Powered by a trained Random Forest model.
- **Modern Web UI**: Responsive, user-friendly HTML form with live predictions.
- **REST API**: Batch and single-customer predictions via `/predict` endpoint.
- **Automated CI/CD**: Every push is tested, containerized, and deployed to Azure.
- **Cloud-Native**: Runs on scalable, secure Azure Container Apps.
- **Secrets Management**: All credentials handled securely via GitHub Secrets.
- **Production-Ready**: Modular, maintainable, and easy to extend.

---

## 🏗️ Architecture

```
User (Web/API)
   │
   ▼
Azure Container App (FastAPI + ML Model)
   │
   ▼
Docker Hub (Image Registry)
   │
   ▼
GitHub Actions (CI/CD)
```

---

## 📸 Screenshot

<!-- Replace with an actual screenshot if available -->
![Web UI Screenshot](docs/screenshot.png)

---

## 📁 Project Structure

```
CustomerChurn_Prediction/
├── app.py                  # FastAPI app (API + HTML frontend)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker build instructions
├── models/                 # ML model, preprocessor, columns
│   ├── preprocessor.pkl
│   ├── random_forest_churn_from_script.pkl
│   └── model_columns.pkl
├── templates/
│   └── index.html          # Jinja2 HTML template
├── src/                    # (Optional) Data prep, training scripts
│   ├── preprocessing.py
│   ├── train_model.py
│   └── test.py
├── tests/                  # Unit and API tests
│   └── test_api.py
└── .github/workflows/ci.yml # GitHub Actions workflow
```

---

## ⚡ Quickstart

### 1. **Clone & Install**
```bash
git clone https://github.com/ManojRam7/CustomerChurn_Prediction.git
cd CustomerChurn_Prediction
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. **Run Locally**
```bash
uvicorn app:app --reload --port 8080
```
- Visit [http://localhost:8080](http://localhost:8080) for the web UI.
- Use `/predict` for API requests.

### 3. **Run Tests**
```bash
pytest --cov=src --cov=app --cov-report=term
```

---

## 🐳 Docker

### **Build & Run Locally**
```bash
docker build --platform linux/amd64 -t manojram7/customer-churn-api:latest .
docker run -p 8080:8080 manojram7/customer-churn-api:latest
```

---

## ☁️ Azure Deployment

1. **Push Docker image to Docker Hub:**
    ```bash
    docker push manojram7/customer-churn-api:latest
    ```
2. **Deploy via Azure Portal or CLI:**
    - Use image: `manojram7/customer-churn-api:latest`
    - Set target port: `8080`
    - Enable ingress for public access

---

## 🔄 CI/CD Integration

This project uses **GitHub Actions** for end-to-end automation:

- **On every push or PR to `main`:**
  - Checks out code
  - Installs dependencies
  - Runs all tests with coverage
  - Builds and pushes Docker image to Docker Hub
  - Deploys the new image to Azure Container Apps

### **Workflow Highlights**
- **Secrets**: All credentials (Docker Hub, Azure) are stored securely in GitHub Secrets.
- **Traceability**: Docker images are tagged with commit SHA.
- **Zero-downtime**: Azure Container App is updated automatically.

<details>
<summary>Click to view CI/CD workflow YAML</summary>

```yaml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-test-deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Install coverage
      run: pip install pytest-cov

    - name: Run tests with coverage
      run: |
        PYTHONPATH=. pytest --cov=src --cov=app --cov-report=term

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Log in to Docker Hub
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}

    - name: Build and push Docker image (amd64)
      run: |
        docker buildx build --platform linux/amd64 \
          -t manojram7/customer-churn-api:${{ github.sha }} \
          --push .

    - name: Azure Login
      uses: azure/login@v2
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}

    - name: Deploy to Azure Container App
      run: |
        az account set --subscription ${{ secrets.AZURE_SUBSCRIPTION_ID }}
        az containerapp update \
          --name ${{ secrets.AZURE_CONTAINERAPP_NAME }} \
          --resource-group ${{ secrets.AZURE_RESOURCE_GROUP }} \
          --image manojram7/customer-churn-api:${{ github.sha }}
```
</details>

---

## 🧪 API Example (Postman)

**POST** `/predict`
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
      "Contract_Length": "Quarterly",
      "Total_Spend": 1200.50,
      "Last_Interaction": 5
    }
  ]
}
```

---

## 🔒 Security & Best Practices

- All secrets are managed via GitHub Actions secrets.
- Docker images are built for `linux/amd64` for maximum compatibility.
- Model files are versioned and included in the repo for reproducibility.
- Automated tests ensure reliability before every deployment.

---

## 📈 Roadmap & Enhancements

- [ ] Add authentication for API endpoints
- [ ] Integrate monitoring/logging (Azure Monitor, App Insights)
- [ ] Add blue/green deployment support
- [ ] Expand test coverage

---

## 🙌 Contributing

Pull requests and issues are welcome!  
For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

MIT License

---

**Happy Predicting! 🚀**