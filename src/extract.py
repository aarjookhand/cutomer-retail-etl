from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "raw" / "customer_data.csv"

def extract_customer_data()-> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    return df