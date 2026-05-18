import unittest
from unittest.mock import patch

from scripts.fetch_data import main


class TestFetchScript(unittest.TestCase):
    @patch("scripts.fetch_data.fetch_data")
    def test_fetch_script_uses_output_flag(self, mock_fetch_data):
        mock_fetch_data.return_value = "data/raw/creditcard.parquet"

        with patch(
            "sys.argv", ["fetch_data.py", "--output", "data/raw/creditcard.parquet"]
        ):
            main()

        mock_fetch_data.assert_called_once_with("data/raw/creditcard.parquet")


if __name__ == "__main__":
    unittest.main()
