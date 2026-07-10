import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Connection


CREATE_CUSTOMER_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    gender VARCHAR(20),
    age INTEGER,
    city VARCHAR(100),
    membership_type VARCHAR(20),
    total_spend NUMERIC(10, 2),
    items_purchased INTEGER,
    average_rating NUMERIC(3, 2),
    discount_applied BOOLEAN,
    days_since_last_purchase INTEGER,
    satisfaction_level VARCHAR(20)
);
"""


INSERT_CUSTOMER_QUERY = """
INSERT INTO customers (
    customer_id,
    gender,
    age,
    city,
    membership_type,
    total_spend,
    items_purchased,
    average_rating,
    discount_applied,
    days_since_last_purchase,
    satisfaction_level
)
VALUES (
    :customer_id,
    :gender,
    :age,
    :city,
    :membership_type,
    :total_spend,
    :items_purchased,
    :average_rating,
    :discount_applied,
    :days_since_last_purchase,
    :satisfaction_level
)
ON CONFLICT (customer_id) DO NOTHING;
"""


def create_customer_table(connection: Connection) -> None:
    connection.execute(text(CREATE_CUSTOMER_TABLE_QUERY))


def insert_customer_data(
    connection: Connection,
    df: pd.DataFrame,
) -> None:
    customer_records = df.to_dict(orient="records")

    connection.execute(
        text(INSERT_CUSTOMER_QUERY),
        customer_records,
    )