from typing import Any


def train_model(model: Any, X: Any, y: Any) -> Any:
    """Train a model with provided data."""
    model.fit(X, y)
    return model
