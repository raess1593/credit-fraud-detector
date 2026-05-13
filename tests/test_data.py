import pandas as pd
import unittest
from unittest.mock import patch, Mock
from src.data import load_data

class TestDataLoading(unittest.TestCase):
    
    @patch("src.data.load_dataset")
    def test_load_data(self, mock_load_dataset):
        """Test if load_data function returns X and y dataframes"""
        mock_hf = Mock()
        mock_hf.to_pandas.return_value = pd.DataFrame({"Feature1": [1, 2], "Class": [0, 1]})
        mock_load_dataset.return_value = {"train": mock_hf}

        X, y = load_data()
        
        self.assertIsNotNone(X)
        self.assertIsNotNone(y)
        self.assertEqual(len(X), len(y))
        self.assertEqual(y.name, "Class")

    @patch("src.data.load_dataset")
    def test_load_data_exception(self, mock_load_dataset):
        """Test if load_data function raises an exception when dataset is not found"""
        mock_load_dataset.side_effect = Exception("Dataset not found")

        with self.assertRaises(Exception) as context:
            load_data()
        
        self.assertIn("Dataset not found", str(context.exception))

    @patch("src.data.load_dataset")
    def test_load_data_empty_dataset(self, mock_load_dataset):
        """Test if load_data function handles empty dataset correctly"""
        mock_hf = Mock()
        mock_hf.to_pandas.return_value = pd.DataFrame(columns=["Class"])
        mock_load_dataset.return_value = {"train": mock_hf}

        X, y = load_data()
        
        self.assertTrue(X.empty)
        self.assertTrue(y.empty)

if __name__ == "__main__":
    unittest.main()