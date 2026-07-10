from sqlalchemy import create_engine, text
from src.config import DATABASE_URL
from src.utils.logger import logger

engine = create_engine(DATABASE_URL)

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            logger.info("Database connection successful: %s", result.fetchone())
    except Exception as e:
        logger.error("Database connection failed: %s", e)