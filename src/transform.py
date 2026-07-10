import pandas as pd

def transform_customer_data(df: pd.DataFrame) -> pd.DataFrame:
    transformed_df = df.copy()

    transformed_df.columns = (
        transformed_df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    text_columns = [
        "gender",
        "city",
        "membership_type",
        "satisfaction_level",
    ]

    for column in text_columns:
        transformed_df[column] = (
            transformed_df[column]
            .str.strip()
            .str.lower()
        )

    transformed_df["customer_id"] = transformed_df["customer_id"].astype(int)

    transformed_df["age"] = transformed_df["age"].astype(int)

    transformed_df["total_spend"] = transformed_df["total_spend"].astype(float)

    transformed_df["items_purchased"] = transformed_df["items_purchased"].astype(int)

    transformed_df["average_rating"] = transformed_df["average_rating"].astype(float)

    transformed_df["days_since_last_purchase"] = transformed_df["days_since_last_purchase"].astype(int)

    return transformed_df