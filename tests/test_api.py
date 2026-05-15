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
    def test_predict_success(
        self,
        mock_set_tracking_uri,
        mock_set_experiment,
        mock_load_model,
    ):
        mock_model = Mock()
        mock_model.predict.return_value = [1]
        mock_load_model.return_value = mock_model

        result = predict(build_transaction_input())

        self.assertEqual(result, {"prediction": 1})
        mock_model.predict.assert_called_once()

    @patch("api.api.mlflow.pyfunc.load_model")
    @patch("api.api.mlflow.set_experiment")
    @patch("api.api.mlflow.set_tracking_uri")
    def test_predict_production_model_not_found(
        self,
        mock_set_tracking_uri,
        mock_set_experiment,
        mock_load_model,
    ):
        mock_load_model.side_effect = Exception("missing")

        with self.assertRaises(HTTPException) as context:
            predict(build_transaction_input())

        self.assertEqual(context.exception.status_code, 404)
        self.assertIn("Production model not found", context.exception.detail)


if __name__ == "__main__":
    unittest.main()
