from functools import lru_cache
from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
TEMPLATES_DIR = BASE_DIR / "templates"

# External API schema (underscore names) mapped to model schema (space names).
EXTERNAL_TO_INTERNAL = {
    "CustomerID": "CustomerID",
    "Age": "Age",
    "Gender": "Gender",
    "Tenure": "Tenure",
    "Usage_Frequency": "Usage Frequency",
    "Support_Calls": "Support Calls",
    "Payment_Delay": "Payment Delay",
    "Subscription_Type": "Subscription Type",
    "Contract_Length": "Contract Length",
    "Total_Spend": "Total Spend",
    "Last_Interaction": "Last Interaction",
}

FORM_FIELD_ORDER = list(EXTERNAL_TO_INTERNAL.keys())

app = FastAPI(
    title="Customer Churn Prediction API",
    description="Inference API and web form for telecom churn prediction.",
    version="2.0.0",
)
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


class CustomerRow(BaseModel):
    CustomerID: int = Field(..., ge=1)
    Age: int = Field(..., ge=18, le=100)
    Gender: Literal["Male", "Female"]
    Tenure: int = Field(..., ge=0)
    Usage_Frequency: int = Field(..., ge=0)
    Support_Calls: int = Field(..., ge=0)
    Payment_Delay: int = Field(..., ge=0)
    Subscription_Type: Literal["Basic", "Standard", "Premium"]
    Contract_Length: Literal["Monthly", "Quarterly", "Annual"]
    Total_Spend: float = Field(..., ge=0)
    Last_Interaction: int = Field(..., ge=0)

    @field_validator("Total_Spend")
    @classmethod
    def round_total_spend(cls, value: float) -> float:
        return round(value, 2)


class CustomerBatch(BaseModel):
    data: list[CustomerRow] = Field(..., min_length=1)


@lru_cache(maxsize=1)
def load_inference_bundle() -> dict[str, object]:
    preprocessor = joblib.load(MODELS_DIR / "preprocessor.pkl")
    model = joblib.load(MODELS_DIR / "random_forest_churn_from_script.pkl")
    model_columns = joblib.load(MODELS_DIR / "model_columns.pkl")
    return {
        "preprocessor": preprocessor,
        "model": model,
        "model_columns": model_columns,
    }


def _to_internal_dataframe(rows: list[CustomerRow]) -> pd.DataFrame:
    raw = pd.DataFrame([row.model_dump() for row in rows])
    raw = raw[FORM_FIELD_ORDER]
    return raw.rename(columns=EXTERNAL_TO_INTERNAL)


def _predict(rows: list[CustomerRow]) -> tuple[list[int], list[float] | None]:
    bundle = load_inference_bundle()
    frame = _to_internal_dataframe(rows)

    try:
        processed = bundle["preprocessor"].transform(frame)
        processed_df = processed.copy() if isinstance(processed, pd.DataFrame) else pd.DataFrame(processed)

        model_columns = list(bundle["model_columns"])
        if processed_df.shape[1] == len(model_columns):
            processed_df.columns = model_columns
        else:
            processed_df = processed_df.reindex(columns=model_columns, fill_value=0)

        predictions = bundle["model"].predict(processed_df).tolist()

        probabilities = None
        if hasattr(bundle["model"], "predict_proba"):
            churn_proba = bundle["model"].predict_proba(processed_df)[:, 1]
            probabilities = [round(float(p), 4) for p in churn_proba]

        return predictions, probabilities
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail="Unexpected inference error") from error


@app.get("/", response_class=HTMLResponse)
def form_get(request: Request) -> HTMLResponse:
    context = {
        "request": request,
        "prediction": None,
        "probability": None,
        "form_data": {},
    }
    return templates.TemplateResponse("index.html", context)


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
    Last_Interaction: int = Form(...),
) -> HTMLResponse:
    payload = {
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
        "Last_Interaction": Last_Interaction,
    }

    prediction = "Error"
    probability = None

    try:
        row = CustomerRow(**payload)
        predictions, probabilities = _predict([row])
        prediction = "Churn" if predictions[0] == 1 else "No Churn"
        probability = probabilities[0] if probabilities else None
    except Exception as error:
        prediction = f"Error: {error}"

    context = {
        "request": request,
        "prediction": prediction,
        "probability": probability,
        "form_data": payload,
    }
    return templates.TemplateResponse("index.html", context)


@app.post("/predict")
def predict(batch: CustomerBatch) -> dict[str, object]:
    predictions, probabilities = _predict(batch.data)
    response: dict[str, object] = {"predictions": predictions}
    if probabilities is not None:
        response["probabilities"] = probabilities
    return response


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/model_info")
def model_info() -> dict[str, str]:
    bundle = load_inference_bundle()
    return {
        "model": bundle["model"].__class__.__name__,
        "version": "2.0.0",
    }
