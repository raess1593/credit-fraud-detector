from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODELS_CONFIG_DIR = REPO_ROOT / "configs" / "models"


def load_model_config(model_name: str, config_path: str | None = None) -> dict:
    """Load model config from YAML file."""
    path = (
        Path(config_path)
        if config_path
        else DEFAULT_MODELS_CONFIG_DIR / f"{model_name}.yaml"
    )

    with path.open("r", encoding="utf-8") as config_file:
        return yaml.safe_load(config_file) or {}
