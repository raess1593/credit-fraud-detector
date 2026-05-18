import argparse

from src.data import fetch_data


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch dataset to local parquet")
    parser.add_argument(
        "--output",
        default="data/raw/creditcard.parquet",
        help="Output parquet path",
    )
    args = parser.parse_args()

    output_path = fetch_data(args.output)
    print(f"Saved dataset to {output_path}")


if __name__ == "__main__":
    main()
