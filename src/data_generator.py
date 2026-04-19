import pandas as pd
import numpy as np
import os

def generate_climate_data(output_path="data/raw/climate_data.csv"):
    np.random.seed(42)

    dates = pd.date_range(start="2000-01-01", end="2024-12-01", freq="MS")
    regions = ["North", "South", "East", "West", "Central"]

    records = []

    for region in regions:
        base_temp = {
            "North": 18,
            "South": 27,
            "East": 23,
            "West": 24,
            "Central": 25
        }[region]

        base_rain = {
            "North": 55,
            "South": 130,
            "East": 95,
            "West": 80,
            "Central": 70
        }[region]

        base_co2 = 370
        base_sea = 0

        for i, date in enumerate(dates):
            month = date.month

            seasonal_temp = 7 * np.sin((2 * np.pi * month) / 12)
            seasonal_rain = 28 * np.cos((2 * np.pi * month) / 12)

            warming_trend = i * 0.012
            co2_trend = i * 0.20
            sea_trend = i * 0.035

            temperature = base_temp + seasonal_temp + warming_trend + np.random.normal(0, 1.4)
            rainfall = max(0, base_rain + seasonal_rain + np.random.normal(0, 10))
            co2 = base_co2 + co2_trend + np.random.normal(0, 2.5)
            sea_level = base_sea + sea_trend + np.random.normal(0, 0.7)

            # simulated anomalies
            if np.random.rand() < 0.03:
                temperature += np.random.choice([4.5, -4.5])
            if np.random.rand() < 0.03:
                rainfall += np.random.choice([55, -35])
            if np.random.rand() < 0.02:
                co2 += np.random.choice([8, -8])

            records.append([
                date, region, temperature, rainfall, co2, sea_level
            ])

    df = pd.DataFrame(records, columns=[
        "date", "region", "temperature", "rainfall", "co2", "sea_level"
    ])

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Climate dataset generated at: {output_path}")

if __name__ == "__main__":
    generate_climate_data()