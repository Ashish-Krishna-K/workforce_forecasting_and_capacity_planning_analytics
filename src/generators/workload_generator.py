from pathlib import Path

import numpy as np
import pandas as pd

np.random.seed(42)

QUEUE_CONFIG = {
    "Claims": {"base_volume": 850, "base_aht": 450},
    "Billing": {"base_volume": 650, "base_aht": 300},
    "Customer Service": {"base_volume": 1200, "base_aht": 350},
    "Escalations": {"base_volume": 150, "base_aht": 700},
    "Technical Support": {"base_volume": 450, "base_aht": 600},
}

DOW_MULTIPLIER = {0: 1.20, 1: 1.15, 2: 1.05, 3: 1.00, 4: 0.90, 5: 0.70, 6: 0.50}

MONTH_MULTIPLIER = {
    1: 1.00,
    2: 0.98,
    3: 1.00,
    4: 1.08,
    5: 1.12,
    6: 1.10,
    7: 0.92,
    8: 0.90,
    9: 1.08,
    10: 1.12,
    11: 1.15,
    12: 1.25,
}


def create_calendar(start_date: str, end_date: str) -> pd.DataFrame:
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)
    return (
        pd.date_range(start=start_dt, end=end_dt)
        .to_frame(index=False, name="date")
        .assign(
            day_index=lambda df: range(len(df)),
            dow_num=lambda df: df["date"].dt.dayofweek,
            dow_name=lambda df: df["date"].dt.day_name(),
            month_num=lambda df: df["date"].dt.month,
            month_name=lambda df: df["date"].dt.month_name(),
            year=lambda df: df["date"].dt.year,
        )
    )


def validate_calendar(calendar: pd.DataFrame) -> None:
    assert len(calendar) == 731, f"Expected 731 rows, found {len(calendar)}."

    assert calendar["date"].min() == pd.Timestamp("2024-01-01"), (
        f"Expected first date to be '2024-01-01', found {calendar['date'].min().strftime('%Y-%m-%d')}."
    )
    assert calendar["date"].max() == pd.Timestamp("2025-12-31"), (
        f"Expected last date to be '2025-12-31', found {calendar['date'].max().strftime('%Y-%m-%d')}."
    )

    assert calendar["date"].is_unique, "Date column contains duplicates."

    assert calendar.isna().sum().sum() == 0, (
        "Calendar dataframe contains null/na values."
    )

    assert calendar["dow_num"].between(0, 6).all(), (
        "Day of week number is outside the range 0-6."
    )

    assert calendar["month_num"].between(1, 12).all(), (
        "Month number is outside the range 1-12."
    )

    assert calendar["year"].isin([2024, 2025]).all(), "Unexpected year found."

    assert calendar["day_index"].min() == 0, (
        f"Expected minimum day index to be 0, found {calendar['day_index'].min()}."
    )
    assert calendar["day_index"].max() == 730, (
        f"Expected maximum day index to be 730, found {calendar['day_index'].max()}"
    )


def generate_workload(calendar: pd.DataFrame) -> pd.DataFrame:
    queue_df = pd.DataFrame.from_dict(QUEUE_CONFIG, orient="index").reset_index(
        names="queue"
    )
    total_days = len(calendar)
    return pd.merge(calendar, queue_df, how="cross").assign(
        volume=lambda df: (
            (
                df["base_volume"]
                * df["dow_num"].map(DOW_MULTIPLIER)
                * df["month_num"].map(MONTH_MULTIPLIER)
                * (1 + (df["day_index"] / total_days) * 0.08)
                * (np.random.normal(loc=1, scale=0.08, size=len(df)))
            )
            .round()
            .clip(lower=1)
            .astype(int)
        ),
        aht_seconds=lambda df: (
            (df["base_aht"] * (np.random.normal(loc=1, scale=0.05, size=len(df))))
            .round()
            .clip(lower=60)
            .astype(int)
        ),
        workload_seconds=lambda df: df["volume"] * df["aht_seconds"],
    )[["date", "queue", "volume", "aht_seconds", "workload_seconds"]]


def validate_workload(workload: pd.DataFrame) -> None:
    expected_queues = set(QUEUE_CONFIG.keys())

    assert len(workload) == 731 * len(expected_queues), (
        f"Expected row count of {731 * len(expected_queues)}, found {len(workload)}."
    )

    assert workload.isna().sum().sum() == 0, (
        "Workload dataframe contains null/na values."
    )

    assert workload["date"].min() == pd.Timestamp("2024-01-01"), (
        f"Expected first date to be '2024-01-01', found {workload['date'].min().strftime('%Y-%m-%d')}."
    )
    assert workload["date"].max() == pd.Timestamp("2025-12-31"), (
        f"Expected last date to be '2025-12-31', found {workload['date'].max().strftime('%Y-%m-%d')}."
    )

    assert set(workload["queue"].unique()) == expected_queues, "Unexpected queue found."

    assert workload["volume"].gt(0).all(), "Found zero or negative volume."

    assert workload["aht_seconds"].ge(60).all(), (
        "Found a row with aht_second less than 60 seconds."
    )

    assert workload["workload_seconds"].gt(0).all(), (
        "Found zero or negative workload second."
    )

    assert (
        workload["workload_seconds"] == workload["volume"] * workload["aht_seconds"]
    ).all(), "Incorrect workload seconds value found."

    assert workload.groupby(["date", "queue"]).size().eq(1).all(), (
        "Duplicate date-queue combination found."
    )

    assert workload.groupby("queue").size().eq(731).all(), (
        "Total queue counts does not equal to 731"
    )


def generate_shrinkage(calendar: pd.DataFrame) -> pd.DataFrame:
    base_shrinkage_map = {
        i: 0.33 if i == 12 else 0.31 if i in (6, 7, 8) else 0.3 for i in range(1, 13)
    }
    return calendar.assign(
        shrinkage_pct=lambda df: (
            (
                df["month_num"].map(base_shrinkage_map)
                + (np.random.normal(loc=0, scale=0.015, size=len(df)))
            )
            .clip(lower=0.25, upper=0.4)
            .round(4)
        )
    )[["date", "shrinkage_pct"]]


def validate_shrinkage(shrinkage: pd.DataFrame) -> None:
    assert len(shrinkage) == 731, "Row count is not 731."

    assert shrinkage.isna().sum().sum() == 0, (
        "Shrinkage dataframe contains null/na values."
    )

    assert shrinkage["date"].is_unique, "Duplicate dates found."

    assert shrinkage["date"].min() == pd.Timestamp("2024-01-01"), (
        f"Expected first date to be '2024-01-01', found {shrinkage['date'].min().strftime('%Y-%m-%d')}."
    )
    assert shrinkage["date"].max() == pd.Timestamp("2025-12-31"), (
        f"Expected last date to be '2025-12-31', found {shrinkage['date'].max().strftime('%Y-%m-%d')}."
    )

    assert shrinkage["shrinkage_pct"].between(0.25, 0.40).all(), (
        "Shrinkage percentage is not falling within the range of 25%-40%."
    )

    assert shrinkage["shrinkage_pct"].mean() > 0.28, (
        "Average shrinkage percentage is below 28%."
    )

    assert shrinkage["shrinkage_pct"].mean() < 0.35, (
        "Average shrinkage percentage is above 35%."
    )


def generate_staffing(workload: pd.DataFrame, shrinkage: pd.DataFrame) -> pd.DataFrame:
    variance_list = [0.85, 0.95, 1.00, 1.05, 1.15]
    daily_workload = (
        workload.groupby("date", as_index=False)["workload_seconds"]
        .sum()
        .assign(
            workload_hours=lambda df: df["workload_seconds"] / 3600,
        )
    )
    return pd.merge(daily_workload, shrinkage, on="date").assign(
        required_fte=lambda df: (df["workload_hours"] / 8).round(1),
        shrinkage_adjusted_fte=lambda df: (
            df["required_fte"] / (1 - df["shrinkage_pct"])
        ).round(1),
        scheduled_fte=lambda df: (
            (
                df["shrinkage_adjusted_fte"]
                * (np.random.choice(variance_list, size=len(df)))
            )
            .round()
            .astype(int)
        ),
    )[["date", "required_fte", "shrinkage_adjusted_fte", "scheduled_fte"]]


def validate_staffing(staffing: pd.DataFrame) -> None:
    assert len(staffing) == 731, "Row count is not 731."

    assert staffing.isna().sum().sum() == 0, (
        "Staffing dataframe contains null/na values."
    )

    assert staffing["date"].is_unique, "Duplicate dates found."

    assert staffing["scheduled_fte"].gt(0).all(), (
        "Found zero or negative scheduled fte."
    )

    assert staffing["scheduled_fte"].dtype in (
        np.int64,
        np.int32,
        int,
    ), "scheduled_fte column is not stored as int data type."

    assert staffing["date"].min() == pd.Timestamp("2024-01-01"), (
        f"Expected first date to be '2024-01-01', found {staffing['date'].min().strftime('%Y-%m-%d')}."
    )
    assert staffing["date"].max() == pd.Timestamp("2025-12-31"), (
        f"Expected last date to be '2025-12-31', found {staffing['date'].max().strftime('%Y-%m-%d')}."
    )


def export_to_csv(
    workload: pd.DataFrame,
    shrinkage: pd.DataFrame,
    staffing: pd.DataFrame,
    output_path: Path,
) -> None:

    output_dir.mkdir(parents=True, exist_ok=True)

    workload_file_path = output_path / "fact_workload.csv"
    workload[["date", "queue", "volume", "aht_seconds"]].to_csv(
        workload_file_path, index=False
    )
    print(f"Created {workload_file_path}")

    shrinkage_file_path = output_path / "shrinkage.csv"
    shrinkage[["date", "shrinkage_pct"]].to_csv(shrinkage_file_path, index=False)
    print(f"Created {shrinkage_file_path}")

    staffing_file_path = output_path / "staffing_plan.csv"
    staffing[["date", "scheduled_fte"]].to_csv(staffing_file_path, index=False)
    print(f"Created {staffing_file_path}")


def validate_relationships(
    calendar: pd.DataFrame,
    workload: pd.DataFrame,
    shrinkage: pd.DataFrame,
    staffing: pd.DataFrame,
) -> None:

    calendar_dates = set(calendar["date"])

    assert set(workload["date"]) == calendar_dates, (
        "Workload dataset date coverage does not match calendar dataset."
    )

    assert set(shrinkage["date"]) == calendar_dates, (
        "Shrinkage dataset date coverage does not match calendar dataset."
    )

    assert set(staffing["date"]) == calendar_dates, (
        "Staffing dataset date coverage does not match calendar dataset."
    )

    workload_dates = set(workload.groupby("date").size().index)

    assert workload_dates == calendar_dates, (
        "One or more dates are missing from workload transactions."
    )

    assert set(shrinkage["date"]) == set(staffing["date"]), (
        "Shrinkage and staffing datasets contain different date ranges."
    )


try:
    calendar_df = create_calendar(start_date="2024-01-01", end_date="2025-12-31")
    validate_calendar(calendar=calendar_df)
except AssertionError as e:
    raise AssertionError(f"Calendar dataframe validation failed. {e}") from e

try:
    workload_df = generate_workload(calendar_df)
    validate_workload(workload=workload_df)
except AssertionError as e:
    raise AssertionError(f"Workload dataframe validation failed. {e}") from e

try:
    shrinkage_df = generate_shrinkage(calendar_df)
    validate_shrinkage(shrinkage=shrinkage_df)
except AssertionError as e:
    raise AssertionError(f"Shrinkage dataframe validation failed. {e}") from e

try:
    staffing_df = generate_staffing(workload_df, shrinkage_df)
    validate_staffing(staffing=staffing_df)
except AssertionError as e:
    raise AssertionError(f"Staffing dataframe validation failed. {e}") from e

try:
    validate_relationships(
        calendar=calendar_df,
        workload=workload_df,
        shrinkage=shrinkage_df,
        staffing=staffing_df,
    )
    print("\n✓ All validations passed")
    output_dir = (
        Path.home()
        / "da_projects/workforce_forecasting_and_capacity_planning_analytics/data/raw"
    )
    export_to_csv(
        workload=workload_df,
        shrinkage=shrinkage_df,
        staffing=staffing_df,
        output_path=output_dir,
    )
    print("✓ CSV export completed")
except AssertionError as e:
    raise AssertionError(f"Dataframe relationship validation failed. {e}") from e
