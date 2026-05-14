import unittest
from unittest.mock import Mock, patch

from fastapi import HTTPException

from api.api import predict, read_root
from api.schemas import TransactionInput


def build_transaction_input():
    data = {
        "Time": 0.0,
        "Amount": 42.0,
    }
    data.update({f"V{i}": float(i) for i in range(1, 29)})
    return TransactionInput(**data)


class TestAPI(unittest.TestCase):
    def test_read_root(self):
        result = read_root()
        self.assertEqual(
            result, {"message": "Welcome to the Credit Fraud Detector API!"}
        )

    @patch("api.api.mlflow.pyfunc.load_model")
    @patch("api.api.mlflow.set_experiment")
    @patch("api.api.mlflow.set_tracking_uri")
    @patch("api.api.MlflowClient")
    def test_predict_success(
        self,
        mock_client_cls,
        mock_set_tracking_uri,
        mock_set_experiment,
        mock_load_model,
    ):
        mock_client = mock_client_cls.return_value
        mock_experiment = Mock()
        mock_experiment.experiment_id = "exp-1"
        mock_client.get_experiment_by_name.return_value = mock_experiment

        mock_run = Mock()
        mock_run.info.run_id = "run-1"
        mock_client.search_runs.return_value = [mock_run]

        mock_model = Mock()
        mock_model.predict.return_value = [1]
        mock_load_model.return_value = mock_model

        result = predict(build_transaction_input())

        self.assertEqual(result, {"prediction": 1})
        mock_model.predict.assert_called_once()

    @patch("api.api.mlflow.set_experiment")
    @patch("api.api.mlflow.set_tracking_uri")
    @patch("api.api.MlflowClient")
    def test_predict_experiment_not_found(
        self,
        mock_client_cls,
        mock_set_tracking_uri,
        mock_set_experiment,
    ):
        mock_client = mock_client_cls.return_value
        mock_client.get_experiment_by_name.return_value = None

        with self.assertRaises(HTTPException) as context:
            predict(build_transaction_input())

        self.assertEqual(context.exception.status_code, 404)
        self.assertIn("Experiment not found", context.exception.detail)

    @patch("api.api.mlflow.set_experiment")
    @patch("api.api.mlflow.set_tracking_uri")
    @patch("api.api.MlflowClient")
    def test_predict_production_model_not_found(
        self,
        mock_client_cls,
        mock_set_tracking_uri,
        mock_set_experiment,
    ):
        mock_client = mock_client_cls.return_value
        mock_experiment = Mock()
        mock_experiment.experiment_id = "exp-1"
        mock_client.get_experiment_by_name.return_value = mock_experiment
        mock_client.search_runs.return_value = []

        with self.assertRaises(HTTPException) as context:
            predict(build_transaction_input())

        self.assertEqual(context.exception.status_code, 404)
        self.assertIn("Production model not found", context.exception.detail)


if __name__ == "__main__":
    unittest.main()
