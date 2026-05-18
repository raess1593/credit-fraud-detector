import os
from pathlib import Path

import pandas as pd
from datasets import load_dataset
from dotenv import load_dotenv

load_dotenv()


def fetch_data(output_path: str) -> str:
    """Download dataset from HF and persist to parquet."""
    dataset = load_dataset("David-Egea/Creditcard-fraud-detection")
    df = dataset["train"].to_pandas()

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output, index=False)

    return str(output)


def load_data(data_path: str | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load dataset from local parquet or HF and return X and y dataframes."""
    try:
        resolved_path = data_path or os.getenv(
            "DATA_PATH", "data/raw/creditcard.parquet"
        )
        if resolved_path and Path(resolved_path).exists():
            df = pd.read_parquet(resolved_path)
        else:
            dataset = load_dataset("David-Egea/Creditcard-fraud-detection")
            df = dataset["train"].to_pandas()

        X = df.drop(columns=["Class"])
        y = df["Class"]

        return X, y

    except Exception as e:
        raise e
