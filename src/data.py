import pandas as pd
from datasets import load_dataset
from dotenv import load_dotenv

load_dotenv()


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load dataset from HF and return X and y dataframe"""
    try:
        dataset = load_dataset("David-Egea/Creditcard-fraud-detection")
        df = dataset["train"].to_pandas()

        X = df.drop(columns=["Class"])
        y = df["Class"]

        return X, y

    except Exception as e:
        raise e
