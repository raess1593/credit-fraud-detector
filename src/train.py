from typing import Any, Protocol


class TrainableModel(Protocol):
    def fit(self, X: Any, y: Any) -> Any: ...


def train_model(model: TrainableModel, X: Any, y: Any) -> TrainableModel:
    """Train a model with provided data."""
    model.fit(X, y)
    return model
