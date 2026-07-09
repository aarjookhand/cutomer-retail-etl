from src.database import test_connection
from src.extract import extract_customer_data

if __name__ == "__main__":
    test_connection()

    df = extract_customer_data()
    print("CSV data extracted successfully.")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")