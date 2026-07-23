import re
import pandas as pd
import numpy as np


def normalize_year(year):
    if pd.isna(year):
        return None

    year = str(year).strip().upper()

    year = year.replace("FY", "").replace("*", "").strip()

    match = re.search(r"\d{4}", year)
    if match:
        return int(match.group())

    match = re.search(r"\d{2}", year)
    if match:
        yr = int(match.group())
        return 2000 + yr if yr <= 30 else 1900 + yr

    return None


def clean_numeric(value):
    if pd.isna(value):
        return np.nan

    value = str(value).strip()

    if value.upper() in ["", "NA", "N/A", "-", "NULL"]:
        return np.nan

    negative = False

    if value.startswith("(") and value.endswith(")"):
        negative = True
        value = value[1:-1]

    value = (
        value.replace(",", "")
        .replace("₹", "")
        .replace("%", "")
        .replace(" ", "")
    )

    try:
        number = float(value)

        if negative:
            number *= -1

        return number

    except ValueError:
        return np.nan


def clean_text(text):
    if pd.isna(text):
        return None

    text = str(text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_column_names(df):
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
        .str.replace("/", "_", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace(".", "", regex=False)
    )

    return df


def remove_duplicates(df):
    return df.drop_duplicates().reset_index(drop=True)


def fill_missing_values(df):
    numeric_cols = df.select_dtypes(include=["number"]).columns
    object_cols = df.select_dtypes(include=["object"]).columns

    df[numeric_cols] = df[numeric_cols].fillna(0)
    df[object_cols] = df[object_cols].fillna("Unknown")

    return df


def normalize_dataframe(df):
    df = normalize_column_names(df)

    for column in df.columns:
        if df[column].dtype == "object":
            df[column] = df[column].apply(clean_text)

    df = remove_duplicates(df)
    df = fill_missing_values(df)

    return df