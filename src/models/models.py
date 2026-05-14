import importlib
from typing import Any

from sklearn.ensemble import RandomForestClassifier

from src.models.config import load_app_config, load_model_config


def get_model(
    app_config_path: str | None = None, model_config_path: str | None = None
) -> Any:
    """Build and return the active model based on app config."""
    app_config = load_app_config(config_path=app_config_path)
    model_active = app_config.get("model_active", "random_forest")

    if model_active not in {"random_forest", "xgboost"}:
        raise ValueError(f"Unsupported model_active: {model_active}")

    model_config = load_model_config(model_active, config_path=model_config_path)
    params = model_config.get("params", {})

    if model_active == "random_forest":
        return RandomForestClassifier(**params)

    xgboost = importlib.import_module("xgboost")
    return xgboost.XGBClassifier(**params)
