from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env", encoding="utf-8")
print("Loading .env from:", BASE_DIR / ".env")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT") 
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "customer_data.csv"
VALID_OUTPUT_PATH = BASE_DIR / "data" / "validation_output" / "valid_customer_data.csv"
INVALID_OUTPUT_PATH = BASE_DIR / "data" / "validation_output" / "invalid_customer_data.csv"
TRANSFORMED_OUTPUT_PATH = BASE_DIR / "data" / "processed" / "transformed_customer_data.csv"