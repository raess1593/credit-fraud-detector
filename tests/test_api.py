import unittest
from unittest.mock import MagicMock, patch

import numpy as np
from fastapi.testclient import TestClient

import api.api as api_module
from api.api import app, load_production_model


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.valid_payload = {
            "Time": 0.0,
            "Amount": 149.62,
            "V1": -1.359807,
            "V2": -0.072781,
            "V3": 2.536347,
            "V4": 1.378155,
            "V5": -0.338321,
            "V6": 0.462388,
            "V7": 0.239599,
            "V8": 0.098698,
            "V9": 0.363787,
            "V10": 0.090794,
            "V11": -0.5516,
            "V12": -0.617801,
            "V13": -0.99139,
            "V14": -0.311169,
            "V15": 1.468177,
            "V16": -0.470401,
            "V17": 0.207971,
            "V18": 0.025791,
            "V19": 0.403993,
            "V20": 0.251412,
            "V21": -0.018307,
            "V22": 0.277838,
            "V23": -0.110474,
            "V24": 0.066928,
            "V25": 0.128539,
            "V26": -0.189115,
            "V27": 0.133558,
            "V28": -0.021053,
        }

    def tearDown(self):
        api_module.production_model = None
        api_module.production_model_uri = None

    @patch("api.api.get_production_model_uri")
    @patch("api.api.mlflow.pyfunc.load_model")
    @patch("api.api.mlflow.set_experiment")
    @patch("api.api.mlflow.set_tracking_uri")
    def test_load_production_model(
        self, mock_set_uri, mock_set_exp, mock_load_model, mock_get_uri
    ):
        mock_get_uri.return_value = "models:/credit-fraud-detector/Production"
        mock_model = MagicMock()
        mock_load_model.return_value = mock_model

        load_production_model()

        mock_set_uri.assert_called_once()
        mock_set_exp.assert_called_once_with("credit-fraud-detector")
        mock_load_model.assert_called_once_with(
            "models:/credit-fraud-detector/Production"
        )
        self.assertEqual(api_module.production_model, mock_model)
        self.assertEqual(
            api_module.production_model_uri, "models:/credit-fraud-detector/Production"
        )

    def test_predict_model_not_loaded(self):
        api_module.production_model = None
        response = self.client.post("/predict", json=self.valid_payload)
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["detail"], "Model not loaded")

    def test_predict_success(self):
        mock_model = MagicMock()
        mock_model.predict.return_value = np.array([1])
        api_module.production_model = mock_model

        response = self.client.post("/predict", json=self.valid_payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"prediction": 1})
        mock_model.predict.assert_called_once()
