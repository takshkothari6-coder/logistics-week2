"""Week 2 Logistics Data Collection, Cleaning and Preprocessing.
Place the downloaded public dataset at raw/yellow_tripdata.parquet.
"""
from pathlib import Path
import pandas as pd

RAW = Path("raw/yellow_tripdata.parquet")
CLEAN = Path("processed/logistics_cleaned.parquet")

def preprocess(df):
    df = df.copy()
    df["pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"], errors="coerce")
    df["dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"], errors="coerce")
    print("Missing % (top):")
    print(df.isna().mean().mul(100).sort_values(ascending=False).head(15))
    print("Duplicates before:", df.duplicated().sum())
    df = df.drop_duplicates()
    df["duration_min"] = (
        df["dropoff_datetime"] - df["pickup_datetime"]
    ).dt.total_seconds() / 60
    df = df.dropna(subset=["pickup_datetime","dropoff_datetime","PULocationID"])
    df = df[
        (df["duration_min"] > 0) &
        (df["trip_distance"] >= 0) &
        (df["dropoff_datetime"] >= df["pickup_datetime"])
    ].copy()
    df["date"] = df["pickup_datetime"].dt.date
    df["hour"] = df["pickup_datetime"].dt.hour
    df["weekday"] = df["pickup_datetime"].dt.dayofweek
    df["is_weekend"] = df["weekday"] >= 5
    q1 = df["trip_distance"].quantile(.25)
    q3 = df["trip_distance"].quantile(.75)
    iqr = q3 - q1
    df["distance_outlier"] = (
        (df["trip_distance"] < max(0, q1-1.5*iqr)) |
        (df["trip_distance"] > q3+1.5*iqr)
    )
    return df

def main():
    if not RAW.exists():
        raise FileNotFoundError(f"Download the dataset to {RAW}")
    df = preprocess(pd.read_parquet(RAW))
    print("Final rows:", len(df))
    print("Duplicates after:", df.duplicated().sum())
    print(df[["trip_distance","duration_min"]].describe())
    CLEAN.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(CLEAN, index=False)
    print("Saved:", CLEAN)

if __name__ == "__main__":
    main()
