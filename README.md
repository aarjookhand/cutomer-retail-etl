# Customer Retail ETL Pipeline

## Overview

This project is an end-to-end ETL pipeline built with Python and PostgreSQL. It processes customer retail data from a CSV file (an E-commerce Customer Behavior Dataset obtained from Kaggle) validates data quality, transforms the dataset into a standardized format, and loads the cleaned records into a PostgreSQL database.

Dataset: https://www.kaggle.com/datasets/uom190346a/e-commerce-customer-behavior-dataset

## Features

* Extract customer data from CSV file
* Validate required fields and business rules
* Separate valid and invalid records
* Generate validation reports
* Standardize and clean data
* Load validated records into PostgreSQL
* Track pipeline execution status
* Structured logging throughout the pipeline
* Unit and integration tests with Pytest
* Automated testing using GitHub Actions
* Dockerized application for reproducible environments


## Tech Stack

| Category              | Technologies           |
| --------------------- | ---------------------- |
| Language              | Python 3               |
| Database              | PostgreSQL             |
| Data Processing       | Pandas                 |
| ORM / Database Access | SQLAlchemy             |
| Testing               | Pytest                 |
| CI/CD                 | GitHub Actions         |
| Containerization      | Docker |



## ETL Workflow

```
Raw CSV
    │
    ▼
Extract
    │
    ▼
Validate
    │
    ├── Valid Records
    │       │
    │       ▼
    │   Transform
    │       │
    │       ▼
    │ Load into PostgreSQL
    │
    └── Invalid Records
            │
            ▼
     Saved for Review
```


## Pipeline Monitoring

Each pipeline execution is tracked, including:

* Pipeline status
* Start time
* Completion time
* Number of valid records
* Number of invalid records
* Number of loaded records

This provides visibility into every pipeline run and simplifies debugging.



## Testing

The project includes:

* Unit tests for ETL functions
* Integration tests for PostgreSQL loading
* Automated test execution through GitHub Actions

Run all tests locally:

```bash
pytest
```


## Running the Project

### Clone the repository

```bash
git clone https://github.com/aarjookhand/customer-retail-etl.git
cd customer-retail-etl
```

### Configure environment variables

Create a `.env` file with your PostgreSQL configuration based on the `.env.example` file

### Build and start the containers

```bash
docker compose up --build
```

### Run the pipeline

```bash
python -m src.main
```




## Sample Output

<img width="1378" height="637" alt="image" src="https://github.com/user-attachments/assets/312e5a6a-a908-4ee0-8707-ef512684ee6a" />




## Room for Improvements

* Incremental data loading
* Support for multiple data sources
* Scheduled pipeline execution
* Data quality monitoring dashboard
* Cloud deployment (AWS or Azure)
* Workflow orchestration with Apache Airflow




