import unittest
from unittest.mock import patch

from src.models import load_model


class TestLoadModel(unittest.TestCase):
    @patch("src.models.RandomForestClassifier")
    @patch("src.models.DecisionTreeClassifier")
    def test_load_model_random_forest(self, mock_dt, mock_rf):
        """Test if load_model function returns a RandomForestClassifier instance"""
        mock_rf.return_value = "RandomForestModel"
        model = load_model("random_forest", {"n_estimators": 100})
        self.assertEqual(model, "RandomForestModel")
        mock_rf.assert_called_once_with(n_estimators=100)

    @patch("src.models.RandomForestClassifier")
    @patch("src.models.DecisionTreeClassifier")
    def test_load_model_decision_tree(self, mock_dt, mock_rf):
        """Test if load_model function returns a DecisionTreeClassifier instance"""
        mock_dt.return_value = "DecisionTreeModel"
        model = load_model("decision_tree", {"max_depth": 5})
        self.assertEqual(model, "DecisionTreeModel")
        mock_dt.assert_called_once_with(max_depth=5)

    def test_load_model_invalid_model(self):
        """Test if load_model function raises a ValueError for an invalid model name"""
        with self.assertRaises(ValueError) as context:
            load_model("invalid_model", {})
        self.assertIn("Model is not available", str(context.exception))


if __name__ == "__main__":
    unittest.main()
