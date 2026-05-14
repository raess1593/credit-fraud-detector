from typing import Any

from src.data import load_data
from src.models.models import get_model
from src.train import train_model


def main(config_path: str | None = None) -> Any:
    """Run end-to-end training pipeline."""
    model = get_model(app_config_path=config_path)
    X, y = load_data()
    return train_model(model, X, y)


if __name__ == "__main__":
    main()
