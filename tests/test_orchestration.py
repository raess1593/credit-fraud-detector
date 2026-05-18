import os
import unittest
from unittest.mock import patch

from orchestration import defs


class TestOrchestration(unittest.TestCase):
    @patch("orchestration.defs.fetch_data")
    def test_fetch_data_op_uses_env(self, mock_fetch_data):
        mock_fetch_data.return_value = "data/raw/creditcard.parquet"
        os.environ["DATA_PATH"] = "data/raw/creditcard.parquet"

        result = defs.fetch_data_op()

        self.assertEqual(result, "data/raw/creditcard.parquet")
        mock_fetch_data.assert_called_once_with("data/raw/creditcard.parquet")

        del os.environ["DATA_PATH"]

    @patch("orchestration.defs.run_training")
    def test_train_op_passes_path(self, mock_run_training):
        defs.train_op("data/raw/creditcard.parquet")

        mock_run_training.assert_called_once_with(
            data_path="data/raw/creditcard.parquet"
        )


if __name__ == "__main__":
    unittest.main()
