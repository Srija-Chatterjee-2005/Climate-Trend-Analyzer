import pandas as pd
import numpy as np

def summary_metrics(df):
    return {
        "avg_temperature": round(df["temperature"].mean(), 2),
        "avg_rainfall": round(df["rainfall"].mean(), 2),
        "avg_co2": round(df["co2"].mean(), 2),
        "avg_sea_level": round(df["sea_level"].mean(), 2),
        "records": len(df)
    }

def yearly_trends(df):
    return df.groupby("year")[["temperature", "rainfall", "co2", "sea_level"]].mean().reset_index()

def seasonal_analysis(df):
    season_order = ["Winter", "Spring", "Summer", "Autumn"]
    result = df.groupby("season")[["temperature", "rainfall", "co2", "sea_level"]].mean().reset_index()
    result["season"] = pd.Categorical(result["season"], categories=season_order, ordered=True)
    return result.sort_values("season")

def region_comparison(df):
    return df.groupby("region")[["temperature", "rainfall", "co2", "sea_level"]].mean().reset_index()

def decade_comparison(df):
    return df.groupby("decade")[["temperature", "rainfall", "co2", "sea_level"]].mean().reset_index()

def detect_anomalies(df, column="temperature", threshold=2.0):
    data = df.copy()
    mean = data[column].mean()
    std = data[column].std()

    if std == 0:
        data["z_score"] = 0
        data["anomaly"] = False
        return data

    data["z_score"] = (data[column] - mean) / std
    data["anomaly"] = data["z_score"].abs() > threshold
    return data

def top_anomaly_years(df, column="temperature", threshold=2.0):
    anomaly_df = detect_anomalies(df, column=column, threshold=threshold)
    yearly = (
        anomaly_df[anomaly_df["anomaly"]]
        .groupby("year")
        .size()
        .reset_index(name="anomaly_count")
        .sort_values("anomaly_count", ascending=False)
    )
    return yearly.head(10)

def correlation_table(df):
    return df[["temperature", "rainfall", "co2", "sea_level"]].corr()