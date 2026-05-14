import os

import mlflow
import mlflow.pyfunc
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from mlflow.client import MlflowClient

from api.schemas import TransactionInput

load_dotenv()

app = FastAPI(
    title="Credit Fraud Detector API",
    description="API for detecting credit card fraud using a pre-trained model.",
    version="1.0.0",
)

production_model = None


@app.get("/")
def read_root():
    return {"message": "Welcome to the Credit Fraud Detector API!"}


@app.post("/predict")
def predict(transaction: TransactionInput):
    global production_model

    client = MlflowClient()
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://127.0.1:5000"))
    mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME", "credit-fraud-detector"))

    experiment = client.get_experiment_by_name(
        os.getenv("MLFLOW_EXPERIMENT_NAME", "credit-fraud-detector")
    )
    if experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string="tags.stage = 'production'",
        order_by=["metrics.test_f1 DESC"],
        max_results=1,
    )
    if not runs:
        raise HTTPException(status_code=404, detail="Production model not found")
    best_run = runs[0]
    model_uri = f"runs:/{best_run.info.run_id}/model"
    if production_model is None:
        production_model = mlflow.pyfunc.load_model(model_uri)
    if production_model is None:
        raise HTTPException(status_code=500, detail="Failed to load production model")

    input_data = pd.DataFrame([transaction.model_dump()])
    prediction = production_model.predict(input_data)
    return {"prediction": int(prediction[0])}
