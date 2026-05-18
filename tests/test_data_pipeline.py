import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd

from src.data import fetch_data, load_data


class TestDataPipeline(unittest.TestCase):
    @patch("src.data.load_dataset")
    def test_fetch_data_writes_parquet(self, mock_load_dataset):
        mock_hf = Mock()
        mock_hf.to_pandas.return_value = pd.DataFrame(
            {"Feature1": [1, 2], "Class": [0, 1]}
        )
        mock_load_dataset.return_value = {"train": mock_hf}

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "data" / "creditcard.parquet"
            result = fetch_data(str(output_path))

            self.assertEqual(result, str(output_path))
            self.assertTrue(output_path.exists())

    def test_load_data_from_parquet(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "creditcard.parquet"
            df = pd.DataFrame({"Feature1": [1, 2], "Class": [0, 1]})
            df.to_parquet(output_path, index=False)

            X, y = load_data(data_path=str(output_path))

            self.assertEqual(list(X.columns), ["Feature1"])
            self.assertEqual(y.name, "Class")
            self.assertEqual(len(X), 2)

    @patch("src.data.load_dataset")
    def test_load_data_fallback_to_hf(self, mock_load_dataset):
        mock_hf = Mock()
        mock_hf.to_pandas.return_value = pd.DataFrame(
            {"Feature1": [1, 2], "Class": [0, 1]}
        )
        mock_load_dataset.return_value = {"train": mock_hf}

        X, y = load_data(data_path="/tmp/missing.parquet")

        self.assertEqual(list(X.columns), ["Feature1"])
        self.assertEqual(y.name, "Class")


if __name__ == "__main__":
    unittest.main()
