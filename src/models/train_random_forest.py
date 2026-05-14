from sklearn.ensemble import RandomForestClassifier

from src.data import load_data
from src.models.config import load_model_config


def train_random_forest(config_path: str | None = None) -> RandomForestClassifier:
    """Train a Random Forest model using configurable YAML parameters."""
    config = load_model_config("random_forest", config_path=config_path)
    params = config.get("params", {})

    X, y = load_data()
    model = RandomForestClassifier(**params)
    model.fit(X, y)

    return model


if __name__ == "__main__":
    train_random_forest()
