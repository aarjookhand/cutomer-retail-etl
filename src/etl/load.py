import pandas as pd
from src.db.schema import create_customer_table, insert_customer_data   
from sqlalchemy import text
from src.db.database import engine
from src.utils.logger import logger

def load_customer_data(df: pd.DataFrame) -> None:
    try:
        with engine.begin() as connection:
            create_customer_table(connection)
            insert_customer_data(connection, df)
        logger.info(f"{len(df)} rows of customer data loaded into the database successfully.")
    except Exception as e:
        logger.error("Error loading customer data into the database:", e)
