from pathlib import Path
import pandas as pd
from src.utils.logger import logger

def extract_customer_data(file_path):
    df = pd.read_csv(file_path)
    logger.info(f"CSV data extracted successfully. Rows: {len(df)}, Columns: {len(df.columns)}")
    return df