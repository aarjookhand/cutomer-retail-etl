from sqlalchemy import text
from sqlalchemy.engine import Connection
import json


CREATE_PIPELINE_RUNS_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id SERIAL PRIMARY KEY,
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    status VARCHAR(20) NOT NULL
        CHECK (status IN ('RUNNING', 'SUCCESS', 'FAILED')),
    extracted_rows INTEGER DEFAULT 0,
    valid_rows INTEGER DEFAULT 0,
    invalid_rows INTEGER DEFAULT 0,
    loaded_rows INTEGER DEFAULT 0,
    validation_report JSONB,
    error_message TEXT
);
"""


START_PIPELINE_RUN_QUERY = """
INSERT INTO pipeline_runs (status)
VALUES ('RUNNING')
RETURNING run_id;
"""


COMPLETE_PIPELINE_RUN_QUERY = """
UPDATE pipeline_runs
SET
    status = 'SUCCESS',
    completed_at = CURRENT_TIMESTAMP,
    extracted_rows = :extracted_rows,
    valid_rows = :valid_rows,
    invalid_rows = :invalid_rows,
    loaded_rows = :loaded_rows,
    validation_report = CAST(:validation_report AS JSONB),
    error_message = NULL
WHERE run_id = :run_id;
"""


FAIL_PIPELINE_RUN_QUERY = """
UPDATE pipeline_runs
SET
    status = 'FAILED',
    completed_at = CURRENT_TIMESTAMP,
    error_message = :error_message
WHERE run_id = :run_id;
"""


def create_pipeline_runs_table(connection: Connection) -> None:
    connection.execute(text(CREATE_PIPELINE_RUNS_TABLE_QUERY))


def start_pipeline_run(connection: Connection) -> int:
    result = connection.execute(text(START_PIPELINE_RUN_QUERY))
    return result.scalar_one()


def complete_pipeline_run(
    connection: Connection,
    run_id: int,
    extracted_rows: int,
    valid_rows: int,
    invalid_rows: int,
    loaded_rows: int,
    validation_report: dict,
) -> None:
    connection.execute(
        text(COMPLETE_PIPELINE_RUN_QUERY),
        {
            "run_id": run_id,
            "extracted_rows": extracted_rows,
            "valid_rows": valid_rows,
            "invalid_rows": invalid_rows,
            "loaded_rows": loaded_rows,
            "validation_report": json.dumps(validation_report),
        },
    )


def fail_pipeline_run(
    connection: Connection,
    run_id: int,
    error_message: str,
) -> None:
    connection.execute(
        text(FAIL_PIPELINE_RUN_QUERY),
        {
            "run_id": run_id,
            "error_message": error_message,
        },
    )