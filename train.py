import os
import time

import mlflow
import mlflow.sklearn
import yaml
from dotenv import load_dotenv
from mlflow.client import MlflowClient
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.data import load_data
from src.models import load_model

load_dotenv()


CONFIG_PATH = "config/config.yaml"
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

model_active = config["model_active"]
model_config = config["models"][model_active]
model_name = os.getenv("MLFLOW_MODEL_NAME", config.get("model_registry_name"))
f1_threshold = config["f1_threshold"]


def wait_for_model_version_ready(client: MlflowClient, name: str, version: str) -> None:
    for _ in range(30):
        details = client.get_model_version(name=name, version=version)
        if details.status == "READY":
            return
        time.sleep(1)


def get_production_f1(client: MlflowClient, name: str) -> tuple[float | None, str | None]:
    versions = client.get_latest_versions(name, stages=["Production"])
    if not versions:
        return None, None
    version = versions[0]
    run = client.get_run(version.run_id)
    return run.data.metrics.get("test_f1"), version.version

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000"))
mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME", "credit-fraud-detector"))
mlflow.autolog()

if not model_name:
    raise ValueError("Missing model registry name. Set MLFLOW_MODEL_NAME or config model_registry_name.")

with mlflow.start_run(run_name=f"{model_active}_run"):
    print(f"Training {model_active} with config: {model_config}")
    X, y = load_data()
    model = load_model(model_name=model_active, hyperparameters=model_config)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, shuffle=True, random_state=config["seed"]
    )

    print(f"Train set size: {len(X_train)}, Test set size: {len(X_test)}")
    pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("model", model),
        ]
    )

    print("Fitting the model...")
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    metrics = {
        "test_accuracy": accuracy_score(y_test, y_pred),
        "test_precision": precision_score(y_test, y_pred),
        "test_recall": recall_score(y_test, y_pred),
        "test_f1": f1_score(y_test, y_pred),
    }
    mlflow.log_metrics(metrics)

    mlflow.sklearn.log_model(pipeline, artifact_path="model")
    run_id = mlflow.active_run().info.run_id
    model_uri = f"runs:/{run_id}/model"
    client = MlflowClient()
    registered = mlflow.register_model(model_uri, model_name)
    wait_for_model_version_ready(client, model_name, registered.version)

    new_f1 = metrics["test_f1"]
    if new_f1 >= f1_threshold:
        prod_f1, _ = get_production_f1(client, model_name)
        if prod_f1 is None or new_f1 > prod_f1:
            client.transition_model_version_stage(
                name=model_name,
                version=registered.version,
                stage="Production",
                archive_existing_versions=True,
            )
            mlflow.set_tag("promotion", "production")
        else:
            client.transition_model_version_stage(
                name=model_name,
                version=registered.version,
                stage="Staging",
            )
            mlflow.set_tag("promotion", "staging")
    else:
        mlflow.set_tag("promotion", "rejected")

    print("Test metrics:")
    print(metrics)
