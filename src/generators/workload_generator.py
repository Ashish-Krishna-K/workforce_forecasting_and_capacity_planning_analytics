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


calendar_df = create_calendar(start_date="2024-01-01", end_date="2025-12-31")
print(calendar_df.head(10))
workload_df = generate_workload(calendar_df)
print(workload_df.head(10))
# print(len(workload_df))
# print(workload_df["date"].min(), workload_df["date"].max())
# print(workload_df["queue"].value_counts())
# print(workload_df.groupby("queue")["volume"].describe())
# print(workload_df.groupby("date")["volume"].sum())
# print(workload_df.groupby(pd.Grouper(key="date", freq="ME"))["volume"].sum())
shrinkage_df = generate_shrinkage(calendar_df)
print(shrinkage_df.head(10))
# print(shrinkage_df["shrinkage_pct"].describe())
# print(shrinkage_df.groupby(shrinkage_df["date"].dt.month)["shrinkage_pct"].mean())
staffing_df = generate_staffing(workload_df, shrinkage_df)
print(staffing_df.head(10))
