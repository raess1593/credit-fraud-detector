import unittest
from unittest.mock import Mock, patch

import pandas as pd

from src.models.config import load_model_config
from src.models.train_random_forest import train_random_forest
from src.models.train_xgboost import train_xgboost


class TestModelTraining(unittest.TestCase):

    def test_load_model_config_from_default_yaml(self):
        config = load_model_config("random_forest")

        self.assertIn("params", config)
        self.assertIn("n_estimators", config["params"])

    @patch("src.models.train_random_forest.load_data")
    @patch("src.models.train_random_forest.RandomForestClassifier")
    @patch("src.models.train_random_forest.load_model_config")
    def test_train_random_forest_uses_config(
        self, mock_load_model_config, mock_classifier, mock_load_data
    ):
        mock_load_model_config.return_value = {
            "params": {"n_estimators": 50, "random_state": 42}
        }
        mock_load_data.return_value = (
            pd.DataFrame({"Feature1": [1, 2]}),
            pd.Series([0, 1], name="Class"),
        )

        mock_model = Mock()
        mock_classifier.return_value = mock_model

        trained_model = train_random_forest()

        mock_classifier.assert_called_once_with(n_estimators=50, random_state=42)
        mock_model.fit.assert_called_once()
        self.assertEqual(trained_model, mock_model)

    def test_train_xgboost_uses_config(self):
        mock_xgboost_module = Mock()
        mock_model = Mock()
        mock_xgboost_module.XGBClassifier.return_value = mock_model

        with (
            patch(
                "src.models.train_xgboost.load_model_config",
                return_value={"params": {"n_estimators": 100}},
            ) as mock_load_model_config,
            patch(
                "src.models.train_xgboost.load_data",
                return_value=(
                    pd.DataFrame({"Feature1": [1, 2]}),
                    pd.Series([0, 1], name="Class"),
                ),
            ) as mock_load_data,
            patch(
                "src.models.train_xgboost.importlib.import_module",
                return_value=mock_xgboost_module,
            ) as mock_import_module,
        ):
            trained_model = train_xgboost()

        mock_load_model_config.assert_called_once_with("xgboost", config_path=None)
        mock_load_data.assert_called_once()
        mock_import_module.assert_called_once_with("xgboost")
        mock_xgboost_module.XGBClassifier.assert_called_once_with(n_estimators=100)
        mock_model.fit.assert_called_once()
        self.assertEqual(trained_model, mock_model)


if __name__ == "__main__":
    unittest.main()
