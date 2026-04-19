import pandas as pd
import os

def load_data(file_path="data/raw/climate_data.csv"):
    return pd.read_csv(file_path)

def add_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    return "Autumn"

def preprocess_data(df):
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df = df.drop_duplicates()

    numeric_cols = ["temperature", "rainfall", "co2", "sea_level"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].median())

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["season"] = df["month"].apply(add_season)
    df["decade"] = (df["year"] // 10) * 10

    df["temp_rolling_12"] = df.groupby("region")["temperature"].transform(
        lambda x: x.rolling(window=12, min_periods=1).mean()
    )
    df["rain_rolling_12"] = df.groupby("region")["rainfall"].transform(
        lambda x: x.rolling(window=12, min_periods=1).mean()
    )

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/cleaned_climate_data.csv", index=False)

    return df

def data_quality_summary(df):
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "regions": int(df["region"].nunique())
    }