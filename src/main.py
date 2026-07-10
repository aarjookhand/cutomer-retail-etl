from src.database import test_connection
from src.extract import extract_customer_data
from src.validate import validate_and_split_customer_data

if __name__ == "__main__":
    test_connection()

    df = extract_customer_data()
    print("CSV data extracted successfully.")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    valid_df, invalid_df, report = validate_and_split_customer_data(df)

    report.print_summary(
        valid_count=len(valid_df),
        invalid_count=len(invalid_df),
    )

    valid_df.to_csv("data/validation_output/valid_customer_data.csv", index=False)
    print("Valid customer data saved to 'data/validation_output/valid_customer_data.csv'.")

    invalid_df.to_csv("data/validation_output/invalid_customer_data.csv", index=False)   
    print("Invalid customer data saved to 'data/validation_output/invalid_customer_data.csv'.") 