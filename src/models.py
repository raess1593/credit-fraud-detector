from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier


def load_model(model_name: str, hyperparameters: dict):
    models = {
        "random_forest": RandomForestClassifier,
        "decision_tree": DecisionTreeClassifier,
    }

    if model_name not in models:
        raise ValueError("Model is not available")

    return models[model_name](**hyperparameters)
