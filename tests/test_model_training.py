import unittest
from unittest.mock import Mock, patch

import pandas as pd

from src.main import main
from src.models.config import load_app_config, load_model_config
from src.models.models import get_model
from src.train import train_model


class TestModelTraining(unittest.TestCase):

    def test_load_app_config_from_default_yaml(self):
        config = load_app_config()

        self.assertIn("model_active", config)

    def test_load_model_config_from_default_yaml(self):
        config = load_model_config("random_forest")

        self.assertIn("params", config)
        self.assertIn("n_estimators", config["params"])

    @patch("src.models.models.RandomForestClassifier")
    @patch("src.models.models.load_model_config")
    @patch("src.models.models.load_app_config")
    def test_get_model_random_forest(
        self, mock_load_app_config, mock_load_model_config, mock_classifier
    ):
        mock_load_app_config.return_value = {"model_active": "random_forest"}
        mock_load_model_config.return_value = {
            "params": {"n_estimators": 50, "random_state": 42}
        }
        mock_model = Mock()
        mock_classifier.return_value = mock_model

        built_model = get_model()

        mock_load_app_config.assert_called_once_with(config_path=None)
        mock_load_model_config.assert_called_once_with(
            "random_forest", config_path=None
        )
        mock_classifier.assert_called_once_with(n_estimators=50, random_state=42)
        self.assertEqual(built_model, mock_model)

    def test_get_model_xgboost_uses_config(self):
        mock_xgboost_module = Mock()
        mock_model = Mock()
        mock_xgboost_module.XGBClassifier.return_value = mock_model

        with (
            patch(
                "src.models.models.load_app_config",
                return_value={"model_active": "xgboost"},
            ) as mock_load_app_config,
            patch(
                "src.models.models.load_model_config",
                return_value={"params": {"n_estimators": 100}},
            ) as mock_load_model_config,
            patch(
                "src.models.models.importlib.import_module",
                return_value=mock_xgboost_module,
            ) as mock_import_module,
        ):
            built_model = get_model()

        mock_load_app_config.assert_called_once_with(config_path=None)
        mock_load_model_config.assert_called_once_with("xgboost", config_path=None)
        mock_import_module.assert_called_once_with("xgboost")
        mock_xgboost_module.XGBClassifier.assert_called_once_with(n_estimators=100)
        self.assertEqual(built_model, mock_model)

    @patch("src.models.models.load_app_config")
    def test_get_model_unsupported_model_raises(self, mock_load_app_config):
        mock_load_app_config.return_value = {"model_active": "unsupported_model"}

        with self.assertRaises(ValueError):
            get_model()

    def test_train_model_calls_fit(self):
        model = Mock()
        X = pd.DataFrame({"Feature1": [1, 2]})
        y = pd.Series([0, 1], name="Class")

        trained_model = train_model(model, X, y)

        model.fit.assert_called_once_with(X, y)
        self.assertEqual(trained_model, model)

    @patch("src.main.train_model")
    @patch("src.main.load_data")
    @patch("src.main.get_model")
    def test_main_orchestrates_pipeline(
        self, mock_get_model, mock_load_data, mock_train_model
    ):
        mock_model = Mock()
        mock_get_model.return_value = mock_model
        mock_load_data.return_value = (
            pd.DataFrame({"Feature1": [1, 2]}),
            pd.Series([0, 1], name="Class"),
        )
        mock_train_model.return_value = mock_model

        result = main()

        mock_get_model.assert_called_once_with(app_config_path=None)
        mock_load_data.assert_called_once()
        mock_train_model.assert_called_once_with(
            mock_model, mock_load_data.return_value[0], mock_load_data.return_value[1]
        )
        self.assertEqual(result, mock_model)


if __name__ == "__main__":
    unittest.main()
