import pandas as pd
import pytest
from src.etl.validate import validate_and_split_customer_data
from test_data.valid_dataframe import create_valid_dataframe


def test_valid_customer_data():
    df = create_valid_dataframe()
    valid_df, invalid_df, report = validate_and_split_customer_data(df)

    assert len(valid_df) == 1
    assert len(invalid_df) == 0
    assert report.errors == []
    assert report.warnings == []


def test_missing_customer_id():
    df = create_valid_dataframe()
    df.loc[0, "Customer ID"] = None

    valid_df, invalid_df, report = validate_and_split_customer_data(df)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1


def test_negative_age_is_restricted():
    df = create_valid_dataframe()
    df.loc[0, "Age"] = -5  

    valid_df, invalid_df, report = validate_and_split_customer_data(df)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1


def test_invalid_membership_type_is_rejected():
    df = create_valid_dataframe()
    df.loc[0, "Membership Type"] = "Platinum"

    valid_df, invalid_df, report = validate_and_split_customer_data(df)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1


def test_missing_reqquired_column_raises_value_error():
    df = create_valid_dataframe()
    df = df.drop(columns=["Age"])

    with pytest.raises(ValueError):
        validate_and_split_customer_data(df)
    

def test_valid_and_invalid_rows_are_split():
    valid_data = create_valid_dataframe()
    
    invalid_data = create_valid_dataframe()
    invalid_data.loc[0, "Customer ID"] = 2
    invalid_data.loc[0, "Total Spend"] = -2

    df = pd.concat([valid_data, invalid_data], ignore_index=True)

    valid_df, invalid_df, report = validate_and_split_customer_data(df)

    assert len(valid_df) == 1
    assert len(invalid_df) == 1
