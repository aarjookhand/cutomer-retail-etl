import pandas as pd
from src.etl.transform import transform_customer_data
from test_data.valid_dataframe import create_valid_dataframe

def test_column_names_are_transformed():
    df = create_valid_dataframe()
    transformed_df = transform_customer_data(df)

    expected_column_names = [
        "customer_id",
        "gender",
        "age",
        "city",
        "membership_type",
        "total_spend",
        "items_purchased",
        "average_rating",
        "discount_applied",
        "days_since_last_purchase",
        "satisfaction_level"
    ]

    assert list(transform_customer_data(transformed_df)) == expected_column_names


def test_text_columns_are_cleaned():
    df = create_valid_dataframe()

    transformed_df = transform_customer_data(df)

    assert transformed_df.loc[0, "gender"] == "female"
    assert transformed_df.loc[0, "city"] == "paris"
    assert transformed_df.loc[0, "membership_type"] == "gold"
    assert transformed_df.loc[0, "satisfaction_level"] == "satisfied"


def test_whitespaces_are_removed():
    df = create_valid_dataframe()
    df.loc[0, "City"] = "   PaRis   "
    transformed_df = transform_customer_data(df)

    assert transformed_df.loc[0, "city"] =="paris"