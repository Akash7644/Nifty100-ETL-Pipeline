from pathlib import Path
import pandas as pd

from normaliser import normalize_dataframe


DATA_FOLDER = Path("data/raw")


HEADER_MAPPING = {
    "companies.xlsx": 1,
    "profitandloss.xlsx": 1,
    "balancesheet.xlsx": 1,
    "cashflow.xlsx": 1,
    "analysis.xlsx": 1,
    "documents.xlsx": 1,
    "prosandcons.xlsx": 1,
    "sectors.xlsx": 0,
    "stock_prices.xlsx": 0,
    "financial_ratios.xlsx": 0,
    "peer_groups.xlsx": 0,
    "market_cap.xlsx": 0,
}


def load_excel(file_name):
    file_path = DATA_FOLDER / file_name

    header = HEADER_MAPPING.get(file_name, 0)

    df = pd.read_excel(file_path, header=header)

    df = normalize_dataframe(df)

    return df


def load_all_files():
    data = {}

    for file_name in HEADER_MAPPING.keys():
        try:
            data[file_name] = load_excel(file_name)
            print(f"Loaded {file_name}")

        except Exception as e:
            print(f"Failed to load {file_name}: {e}")

    return data


if __name__ == "__main__":
    datasets = load_all_files()

    for name, df in datasets.items():
        print("\n", "=" * 50)
        print(name)
        print(df.head())