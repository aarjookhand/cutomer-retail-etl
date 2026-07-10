import pandas as pd
from src.db.schema import create_customer_table, insert_customer_data   
from sqlalchemy import text
from db.database import engine

def load_customer_data(df: pd.DataFrame) -> None:
    try:
        with engine.begin() as connection:
            create_customer_table(connection)
            insert_customer_data(connection, df)
            
        print(f"{len(df)} rows of customer data loaded into the database successfully.")
    except Exception as e:
        print("Error loading customer data into the database:", e)
