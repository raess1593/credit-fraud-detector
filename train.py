import os

import mlflow
import yaml
from dotenv import load_dotenv
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

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000"))
mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME", "credit-fraud-detector"))
mlflow.autolog()

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

    if f1_score(y_test, y_pred) > config["f1_threshold"]:
        mlflow.set_tag("stage", "production")

    print("Test metrics:")
    print(metrics)
