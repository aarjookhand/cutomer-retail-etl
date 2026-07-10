from pathlib import Path
import pandas as pd
import pytest
from src.etl.extract import extract_customer_data


def test_extract_customer_data():
    customer_data = extract_customer_data(Path("tests/test_data/sample_customers.csv"))
    assert not customer_data.empty

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        extract_customer_data(Path("/non_existent_file.csv"))

def test_reads_correct_number_of_rows():
    df = extract_customer_data(Path("tests/test_data/sample_customers.csv"))
    assert len(df) == 2

def test_reads_correct_number_of_columns():
    df = extract_customer_data(Path("tests/test_data/sample_customers.csv"))
    assert len(df.columns) == 11
