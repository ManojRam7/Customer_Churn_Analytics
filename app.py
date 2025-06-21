# code version 3.1 for app.py with frontend integration
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, validator
from typing import List

# Load preprocessor, model, and model columns at startup
preprocessor = joblib.load('models/preprocessor.pkl')
model = joblib.load('models/random_forest_churn_from_script.pkl')
model_columns = joblib.load('models/model_columns.pkl')

app = FastAPI(title="Customer Churn Prediction API")
templates = Jinja2Templates(directory="templates")

# --- HTML Frontend ---
@app.get("/", response_class=HTMLResponse)
def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "prediction": None, "form_data": {}})

@app.post("/", response_class=HTMLResponse)
async def form_post(
    request: Request,
    CustomerID: int = Form(...),
    Age: int = Form(...),
    Gender: str = Form(...),
    Tenure: int = Form(...),
    Usage_Frequency: int = Form(...),
    Support_Calls: int = Form(...),
    Payment_Delay: int = Form(...),
    Subscription_Type: str = Form(...),
    Contract_Length: str = Form(...),
    Total_Spend: float = Form(...),
    Last_Interaction: int = Form(...)
):
    form_data = {
        "CustomerID": CustomerID,
        "Age": Age,
        "Gender": Gender,
        "Tenure": Tenure,
        "Usage_Frequency": Usage_Frequency,
        "Support_Calls": Support_Calls,
        "Payment_Delay": Payment_Delay,
        "Subscription_Type": Subscription_Type,
        "Contract_Length": Contract_Length,
        "Total_Spend": Total_Spend,
        "Last_Interaction": Last_Interaction
    }
    try:
        data = [[
            CustomerID, Age, Gender, Tenure, Usage_Frequency, Support_Calls,
            Payment_Delay, Subscription_Type, Contract_Length, Total_Spend, Last_Interaction
        ]]
        df = pd.DataFrame(data, columns=model_columns)
        processed = preprocessor.transform(df)
        processed = pd.DataFrame(processed, columns=model_columns)
        pred = model.predict(processed)[0]
        prediction = "Churn" if pred == 1 else "No Churn"
    except Exception as e:
        prediction = f"Error: {str(e)}"
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "prediction": prediction, "form_data": form_data}
    )

# --- API Backend (optional, for Postman etc.) ---
class CustomerRow(BaseModel):
    CustomerID: int
    Age: int
    Gender: str
    Tenure: int
    Usage_Frequency: int
    Support_Calls: int
    Payment_Delay: int
    Subscription_Type: str
    Contract_Length: str
    Total_Spend: float
    Last_Interaction: int

    @validator('Gender')
    def gender_allowed(cls, v):
        if v not in ['Male', 'Female']:
            raise ValueError('Gender must be Male or Female')
        return v

    @validator('Subscription_Type')
    def subscription_allowed(cls, v):
        if v not in ['Basic', 'Standard', 'Premium']:
            raise ValueError('Invalid subscription type')
        return v

    @validator('Contract_Length')
    def contract_allowed(cls, v):
        if v not in ['Monthly','Quarterly', 'Annual']:
            raise ValueError('Invalid contract length')
        return v

class CustomerData(BaseModel):
    data: List[CustomerRow]

@app.post("/predict")
def predict(customer_data: CustomerData):
    columns = model_columns
    data_rows = [[
        row.CustomerID, row.Age, row.Gender, row.Tenure, row.Usage_Frequency,
        row.Support_Calls, row.Payment_Delay, row.Subscription_Type,
        row.Contract_Length, row.Total_Spend, row.Last_Interaction
    ] for row in customer_data.data]
    for row in data_rows:
        if len(row) != len(columns):
            raise HTTPException(status_code=400, detail=f"Each row must have {len(columns)} values--[Invalid input shape]")
    try:
        df = pd.DataFrame(data_rows, columns=columns)
        processed = preprocessor.transform(df)
        processed = pd.DataFrame(processed, columns=model_columns)
        preds = model.predict(processed)
        return {"predictions": preds.tolist()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

# --- Utility Endpoints ---
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/model_info")
def model_info():
    return {"model": "RandomForest", "version": "1.0"}

@app.post("/reload_model")
def reload_model():
    global model
    model = joblib.load('models/random_forest_churn_from_script.pkl')
    return {"status": "model reloaded"}









'''

# code version 3.0 for app.py with frondtend integration
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, validator
from typing import List

# Load preprocessor, model, and model columns at startup
preprocessor = joblib.load('models/preprocessor.pkl')
model = joblib.load('models/random_forest_churn_from_script.pkl')
model_columns = joblib.load('models/model_columns.pkl')

app = FastAPI(title="Customer Churn Prediction API")
templates = Jinja2Templates(directory="templates")

# --- HTML Frontend ---
@app.get("/", response_class=HTMLResponse)
def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "prediction": None})

@app.post("/", response_class=HTMLResponse)
async def form_post(
    request: Request,
    CustomerID: int = Form(...),
    Age: int = Form(...),
    Gender: str = Form(...),
    Tenure: int = Form(...),
    Usage_Frequency: int = Form(...),
    Support_Calls: int = Form(...),
    Payment_Delay: int = Form(...),
    Subscription_Type: str = Form(...),
    Contract_Length: str = Form(...),
    Total_Spend: float = Form(...),
    Last_Interaction: int = Form(...)
):
    try:
        data = [[
            CustomerID, Age, Gender, Tenure, Usage_Frequency, Support_Calls,
            Payment_Delay, Subscription_Type, Contract_Length, Total_Spend, Last_Interaction
        ]]
        df = pd.DataFrame(data, columns=model_columns)
        processed = preprocessor.transform(df)
        processed = pd.DataFrame(processed, columns=model_columns)
        pred = model.predict(processed)[0]
        prediction = "Churn" if pred == 1 else "No Churn"
    except Exception as e:
        prediction = f"Error: {str(e)}"
    return templates.TemplateResponse("index.html", {"request": request, "prediction": prediction})

# --- API Backend ---
class CustomerRow(BaseModel):
    CustomerID: int
    Age: int
    Gender: str
    Tenure: int
    Usage_Frequency: int
    Support_Calls: int
    Payment_Delay: int
    Subscription_Type: str
    Contract_Length: str
    Total_Spend: float
    Last_Interaction: int

    @validator('Gender')
    def gender_allowed(cls, v):
        if v not in ['Male', 'Female']:
            raise ValueError('Gender must be Male or Female')
        return v

    @validator('Subscription_Type')
    def subscription_allowed(cls, v):
        if v not in ['Basic', 'Standard', 'Premium']:
            raise ValueError('Invalid subscription type')
        return v

    @validator('Contract_Length')
    def contract_allowed(cls, v):
        if v not in ['Monthly','Quarterly','Annual']:
            raise ValueError('Invalid contract length')
        return v

class CustomerData(BaseModel):
    data: List[CustomerRow]

@app.post("/predict")
def predict(customer_data: CustomerData):
    columns = model_columns
    data_rows = [[
        row.CustomerID, row.Age, row.Gender, row.Tenure, row.Usage_Frequency,
        row.Support_Calls, row.Payment_Delay, row.Subscription_Type,
        row.Contract_Length, row.Total_Spend, row.Last_Interaction
    ] for row in customer_data.data]
    for row in data_rows:
        if len(row) != len(columns):
            raise HTTPException(status_code=400, detail=f"Each row must have {len(columns)} values--[Invalid input shape]")
    try:
        df = pd.DataFrame(data_rows, columns=columns)
        processed = preprocessor.transform(df)
        processed = pd.DataFrame(processed, columns=model_columns)
        preds = model.predict(processed)
        return {"predictions": preds.tolist()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

# --- Utility Endpoints ---
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/model_info")
def model_info():
    return {"model": "RandomForest", "version": "1.0"}

@app.post("/reload_model")
def reload_model():
    global model
    model = joblib.load('models/random_forest_churn_from_script.pkl')
    return {"status": "model reloaded"}

'''




'''
## code version 2.0 for app.py with  backend integration of pydantic model
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List

# Load preprocessor, model, and model columns at startup
preprocessor = joblib.load('models/preprocessor.pkl')
model = joblib.load('models/random_forest_churn_from_script.pkl')
model_columns = joblib.load('models/model_columns.pkl')

app = FastAPI(title="Customer Churn Prediction API")

class CustomerRow(BaseModel):
    CustomerID: int
    Age: int
    Gender: str
    Tenure: int
    Usage_Frequency: int
    Support_Calls: int
    Payment_Delay: int
    Subscription_Type: str
    Contract_Length: str
    Total_Spend: float
    Last_Interaction: int

    @validator('Gender')
    def gender_allowed(cls, v):
        if v not in ['Male', 'Female']:
            raise ValueError('Gender must be Male or Female')
        return v

    @validator('Subscription_Type')
    def subscription_allowed(cls, v):
        if v not in ['Basic', 'Standard', 'Premium']:
            raise ValueError('Invalid subscription type')
        return v

    @validator('Contract_Length')
    def contract_allowed(cls, v):
        if v not in ['Monthly', '12m', '24m', 'Annual']:
            raise ValueError('Invalid contract length')
        return v

class CustomerData(BaseModel):
    data: List[CustomerRow]

@app.post("/predict")
def predict(customer_data: CustomerData):
    columns = model_columns
    print("Expected columns:", columns)
    # Convert list of CustomerRow objects to list of lists in correct order
    data_rows = [[
        row.CustomerID, row.Age, row.Gender, row.Tenure, row.Usage_Frequency,
        row.Support_Calls, row.Payment_Delay, row.Subscription_Type,
        row.Contract_Length, row.Total_Spend, row.Last_Interaction
    ] for row in customer_data.data]
    print("Received data:", data_rows)
    print("Expected number of columns:", len(columns))
    for row in data_rows:
        if len(row) != len(columns):
            raise HTTPException(status_code=400, detail=f"Each row must have {len(columns)} values--[Invalid input shape]")
    try:
        df = pd.DataFrame(data_rows, columns=columns)
        processed = preprocessor.transform(df)
        processed = processed.reindex(columns=model_columns, fill_value=0)
        print("Processed columns (after reindex):", list(processed.columns))
        print(processed.head())
        preds = model.predict(processed)
        return {"predictions": preds.tolist()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/model_info")
def model_info():
    return {"model": "RandomForest", "version": "1.0"}

@app.post("/reload_model")
def reload_model():
    global model
    model = joblib.load('models/random_forest_churn_from_script.pkl')
    return








##  code version 1.0 app.py with basic functionality with backend integration


import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

# Load preprocessor, model, and model columns at startup
preprocessor = joblib.load('models/preprocessor.pkl')
model = joblib.load('models/random_forest_churn_from_script.pkl')
model_columns = joblib.load('models/model_columns.pkl')

app = FastAPI(title="Customer Churn Prediction API")

class CustomerData(BaseModel):
    data: List[List[Any]]  # Each item is a list of feature values

@app.post("/predict")
def predict(customer_data: CustomerData):
    columns = model_columns
    print("Expected columns:", columns)
    print("Received data:", customer_data.data)
    print("Expected number of columns:", len(columns))
    for row in customer_data.data:
        if len(row) != len(columns):
            raise HTTPException(status_code=400, detail=f"Each row must have {len(columns)} values--[Inavlid input shape]")
    try:
        df = pd.DataFrame(customer_data.data, columns=columns)
        processed = preprocessor.transform(df)
        processed = processed.reindex(columns=model_columns, fill_value=0)
        print("Processed columns (after reindex):", list(processed.columns))
        print(processed.head())
        preds = model.predict(processed)
        return {"predictions": preds.tolist()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/model_info")
def model_info():
    return {"model": "RandomForest", "version": "1.0"}

@app.post("/reload_model")
def reload_model():
    global model
    model = joblib.load('models/random_forest_churn_from_script.pkl')  # or update to v2 if you have it
    return {"status": "model reloaded"}
'''





