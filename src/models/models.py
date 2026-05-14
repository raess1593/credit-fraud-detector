import importlib
from typing import Any

from sklearn.ensemble import RandomForestClassifier

from src.models.config import load_app_config, load_model_config

DEFAULT_MODEL = "random_forest"


def get_model(
    app_config_path: str | None = None, model_config_path: str | None = None
) -> Any:
    """Build and return the active model based on app config."""
    app_config = load_app_config(config_path=app_config_path)
    model_active = app_config.get("model_active", DEFAULT_MODEL)

    if model_active not in {"random_forest", "xgboost"}:
        raise ValueError(
            "Unsupported model_active: "
            f"{model_active}. Supported models: random_forest, xgboost"
        )

    model_config = load_model_config(model_active, config_path=model_config_path)
    params = model_config.get("params", {})

    if model_active == "random_forest":
        return RandomForestClassifier(**params)
    elif model_active == "xgboost":
        xgboost = importlib.import_module("xgboost")
        return xgboost.XGBClassifier(**params)

    raise RuntimeError(f"Model selection reached unexpected state: {model_active}")
