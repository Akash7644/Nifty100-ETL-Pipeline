import numpy as np
import pandas as pd

from src.etl.normaliser import (
    normalize_year,
    clean_numeric,
    clean_text,
)


def test_year_1():
    assert normalize_year("FY23") == 2023


def test_year_2():
    assert normalize_year("FY24") == 2024


def test_year_3():
    assert normalize_year("FY22") == 2022


def test_year_4():
    assert normalize_year("2023") == 2023


def test_year_5():
    assert normalize_year("2024") == 2024


def test_year_6():
    assert normalize_year("2025*") == 2025


def test_year_7():
    assert normalize_year("FY 2022") == 2022


def test_year_8():
    assert normalize_year("2023-24") == 2023


def test_year_9():
    assert normalize_year("99") == 1999


def test_year_10():
    assert normalize_year("05") == 2005


def test_year_11():
    assert normalize_year(np.nan) is None


def test_year_12():
    assert normalize_year("") is None


def test_year_13():
    assert normalize_year("abcd") is None


def test_year_14():
    assert normalize_year("FY20") == 2020


def test_year_15():
    assert normalize_year("FY19") == 2019


def test_year_16():
    assert normalize_year("2018") == 2018


def test_year_17():
    assert normalize_year("FY17") == 2017


def test_year_18():
    assert normalize_year("2016*") == 2016


def test_year_19():
    assert normalize_year("FY15") == 2015


def test_year_20():
    assert normalize_year("14") == 2014


def test_numeric_rupee():
    assert clean_numeric("₹1,000") == 1000


def test_numeric_percent():
    assert clean_numeric("15%") == 15


def test_numeric_negative():
    assert clean_numeric("(200)") == -200


def test_numeric_na():
    assert np.isnan(clean_numeric("NA"))


def test_numeric_dash():
    assert np.isnan(clean_numeric("-"))


def test_text_spaces():
    assert clean_text("  Tata Steel  ") == "Tata Steel"


def test_text_multiple_spaces():
    assert clean_text("Reliance     Industries") == "Reliance Industries"


def test_text_none():
    assert clean_text(np.nan) is None


def test_text_empty():
    assert clean_text("") == ""


def test_numeric_float():
    assert clean_numeric("123.45") == 123.45