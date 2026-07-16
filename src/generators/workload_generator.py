import pandas as pd

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
    df = pd.date_range(start=start_dt, end=end_dt).to_frame(index=False, name="date")
    df["dow"] = df["date"].dt.day_name()
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    return df


calendar_df = create_calendar(start_date="2024-01-01", end_date="2025-12-31")
