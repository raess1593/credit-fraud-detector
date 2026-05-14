import importlib
from typing import Any

from src.data import load_data
from src.models.config import load_model_config


def train_xgboost(config_path: str | None = None) -> Any:
    """Train an XGBoost model using configurable YAML parameters."""
    config = load_model_config("xgboost", config_path=config_path)
    params = config.get("params", {})

    xgboost = importlib.import_module("xgboost")
    model = xgboost.XGBClassifier(**params)

    X, y = load_data()
    model.fit(X, y)

    return model


if __name__ == "__main__":
    train_xgboost()
