from src.db.database import engine
from src.db.schema import create_customer_table
from test_data.valid_dataframe import create_valid_dataframe
from src.etl.load import load_customer_data
from src.etl.transform import transform_customer_data
from sqlalchemy import text

def test_load_customer_data():
    df = create_valid_dataframe()

    with engine.begin() as conn:
        create_customer_table(conn)
        conn.execute(text("DELETE FROM customers"))

    load_customer_data(transform_customer_data(df))

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT customer_id, city FROM customers WHERE customer_id = 1")
        ).mappings().first()

    assert result["city"] =="paris"