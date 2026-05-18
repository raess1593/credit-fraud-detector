import os
from contextlib import asynccontextmanager

import mlflow
import mlflow.pyfunc
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from api.schemas import TransactionInput

load_dotenv()

production_model = None
production_model_uri = None


def get_production_model_uri() -> str:
    model_name = os.getenv("MLFLOW_MODEL_NAME", "credit-fraud-detector")
    return f"models:/{model_name}/Production"


def load_production_model() -> None:
    global production_model
    global production_model_uri

    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000"))
    mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME", "credit-fraud-detector"))

    model_uri = get_production_model_uri()
    try:
        production_model = mlflow.pyfunc.load_model(model_uri)
        production_model_uri = model_uri
    except Exception:
        production_model = None
        production_model_uri = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_production_model()
    yield


app = FastAPI(
    title="Credit Fraud Detector API",
    description="API for detecting credit card fraud using a pre-trained model.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Credit Fraud Detector API!"}


@app.post("/predict")
def predict(transaction: TransactionInput):
    global production_model

    if production_model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    input_data = pd.DataFrame([transaction.model_dump()])
    prediction = production_model.predict(input_data)
    return {"prediction": int(prediction[0])}
