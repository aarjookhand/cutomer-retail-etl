from .db.database import test_connection, engine
from .db.pipeline_schema import (create_pipeline_runs_table, start_pipeline_run, complete_pipeline_run, fail_pipeline_run)
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
    run_id = None
    try: 
        logger.info("Starting customer ETL pipeline...")

        with engine.begin() as connection:
            create_pipeline_runs_table(connection)
            run_id = start_pipeline_run(connection)

        logger.info("Pipeline run %s started,", run_id)

        logger.info("Extracting customer data from CSV...")
        raw_df = extract_customer_data(RAW_DATA_PATH)

        logger.info("Validating customer data...")    
        valid_df, invalid_df, report = validate_and_split_customer_data(raw_df)

        report.print_summary(
            valid_count=len(valid_df),      
            invalid_count=len(invalid_df)
        )

        validation_report = {
            "errors": report.errors,
            "warnings": report.warnings,
        }

        logger.info("Saving valid and invalid customer data to respective CSV files...")
        save_dataframe(valid_df, VALID_OUTPUT_PATH, "Valid customer data")
        save_dataframe(invalid_df, INVALID_OUTPUT_PATH, "Invalid customer data")

        logger.info("Transforming valid customer data...")
        transformed_df = transform_customer_data(valid_df)

        logger.info("Saving transformed customer data to CSV...")
        save_dataframe(transformed_df, TRANSFORMED_OUTPUT_PATH, "Transformed customer data")

        logger.info("Loading transformed customer data into the database...")
        load_customer_data(transformed_df)

        with engine.begin() as connection:
            complete_pipeline_run(
                connection=connection,
                run_id=run_id,
                extracted_rows=len(raw_df),
                valid_rows=len(valid_df),
                invalid_rows=len(invalid_df),
                loaded_rows=len(transformed_df),
                validation_report=validation_report
            )

        logger.info("Customer ETL pipeline completed successfully. Run ID: %s", run_id)
    
    except Exception as error:
        logger.exception("Customer ETL pipeline failed")

        if run_id is not None:
            try:
                with engine.begin() as connection:
                    fail_pipeline_run(
                        connection=connection,
                        run_id=run_id,
                        error_message=str(error),
                    )
            except Exception:
                logger.exception("Could not update pipeline run %s to FAILED", run_id )



def main() -> None:
    try:
        test_connection()
        run_pipeline()
    except Exception as e:
        logger.error("Application stopped because the ETL pipeline failed: %s", e)
        return


if __name__ == "__main__":
    test_connection()
    main()