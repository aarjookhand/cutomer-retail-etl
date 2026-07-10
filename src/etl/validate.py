from dataclasses import dataclass, field
import pandas as pd
from src.utils.logger import logger


REQUIRED_COLUMNS = {
    "Customer ID",
    "Gender",
    "Age",
    "City",
    "Membership Type",
    "Total Spend",
    "Items Purchased",
    "Average Rating",
    "Discount Applied",
    "Days Since Last Purchase",
    "Satisfaction Level",
}

VALID_MEMBERSHIPS = {"Bronze", "Silver", "Gold"}
VALID_GENDERS = {"Male", "Female"}
VALID_SATISFACTION_LEVELS = {"Satisfied", "Neutral", "Unsatisfied"}


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def print_summary(self, valid_count: int, invalid_count: int) -> None:
        logger.info("Validation Report:")
        logger.info(f"Valid rows: {valid_count}")
        logger.info(f"Invalid rows: {invalid_count}")

        if self.errors:
            for error in self.errors:
                logger.error(f"{error}")

        if self.warnings:
            for warning in self.warnings:
                logger.warning(f"{warning}")


def validate_and_split_customer_data(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, ValidationReport]:
    report = ValidationReport()

    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        report.errors.append(f"Missing required columns: {sorted(missing_columns)}")
        raise ValueError(report.errors[0])

    df = df.copy()
    df["rejection_reason"] = ""

    def flag(condition, reason: str):
        df.loc[condition, "rejection_reason"] += reason + "; "

    flag(df["Customer ID"].isnull(), "missing customer id")

    flag(df["Age"].isnull(), "missing age")
    flag(df["Age"] < 0, "negative age")

    flag(df["Total Spend"].isnull(), "missing total spend")
    flag(df["Total Spend"] < 0, "negative total spend")

    flag(df["Items Purchased"].isnull(), "missing items purchased")
    flag(df["Items Purchased"] < 0, "negative items purchased")

    flag(df["Average Rating"].isnull(), "missing average rating")
    flag(
        (df["Average Rating"] < 0) | (df["Average Rating"] > 5),
        "average rating outside 0-5",
    )
    flag(df["Membership Type"].isnull(), "missing membership type")    
    flag(df["Membership Type"].notna() & ~df["Membership Type"].isin(VALID_MEMBERSHIPS), "invalid membership type")

    flag(df["Gender"].isnull(), "missing gender")
    flag(df["Gender"].notna() & ~df["Gender"].isin(VALID_GENDERS), "invalid gender")

    flag(df["Satisfaction Level"].isnull(), "missing satisfaction level")
    flag(df["Satisfaction Level"].notna()& ~df["Satisfaction Level"].isin(VALID_SATISFACTION_LEVELS),"invalid satisfaction level",)
    
    flag(df["City"].isnull(), "missing city")
    flag(df["Discount Applied"].isnull(), "missing discount applied")

    invalid_df = df[df["rejection_reason"] != ""].copy()
    valid_df = df[df["rejection_reason"] == ""].drop(columns=["rejection_reason"]).copy()

    if len(invalid_df) > 0:
        report.warnings.append(f"{len(invalid_df)} rows were rejected")
        logger.warning("Rejected rows:")
        for  _, row in invalid_df.iterrows():
            logger.warning(
                f"Customer ID: {row['Customer ID']}, Rejection Reason: {row['rejection_reason']}"
            )

    return valid_df, invalid_df, report