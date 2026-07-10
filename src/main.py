from .db.database import test_connection
from .etl.extract import extract_customer_data
from .etl.validate import validate_and_split_customer_data
from .etl.transform import transform_customer_data
from .etl.load import load_customer_data
from src.utils.logger import logger
from src.config import RAW_DATA_PATH, VALID_OUTPUT_PATH, INVALID_OUTPUT_PATH, TRANSFORMED_OUTPUT_PATH
from pathlib import Path


def save_dataframe(df, output_path:Path, description:str):
    df.to_csv(output_path, index=False)
    logger.info("%s saved to '%s'.", description, output_path)


def run_pipeline()->None:
    logger.info("Starting customer ETL pipeline...")
    logger.info("Extracting customer data from CSV...")
    raw_df = extract_customer_data(RAW_DATA_PATH)

    logger.info("Validating customer data...")    
    valid_df, invalid_df, report = validate_and_split_customer_data(raw_df)

    report.print_summary(
        valid_count=len(valid_df),      
        invalid_count=len(invalid_df)
    )

    logger.info("Saving valid and invalid customer data to respective CSV files...")
    save_dataframe(valid_df, VALID_OUTPUT_PATH, "Valid customer data")
    save_dataframe(invalid_df, INVALID_OUTPUT_PATH, "Invalid customer data")

    logger.info("Transforming valid customer data...")
    transformed_df = transform_customer_data(valid_df)

    logger.info("Saving transformed customer data to CSV...")
    save_dataframe(transformed_df, TRANSFORMED_OUTPUT_PATH, "Transformed customer data")

    logger.info("Loading transformed customer data into the database...")
    load_customer_data(transformed_df)

    logger.info("Customer ETL pipeline completed successfully.")


def main() -> None:
    try:
        run_pipeline()
    except Exception as e:
        logger.error("Customer ETL pipeline failed: %s", e)
        return

if __name__ == "__main__":
    test_connection()
    main()
