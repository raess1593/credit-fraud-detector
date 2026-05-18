import os

from dagster import Definitions, job, op

from src.data import fetch_data
from train import run_training


@op
def fetch_data_op() -> str:
    output_path = os.getenv("DATA_PATH", "data/raw/creditcard.parquet")
    if os.path.exists(output_path):
        return output_path
    return fetch_data(output_path)


@op
def train_op(data_path: str) -> None:
    run_training(data_path=data_path)


@job
def training_job() -> None:
    train_op(fetch_data_op())


defs = Definitions(jobs=[training_job])
