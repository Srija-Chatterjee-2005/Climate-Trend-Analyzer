def generate_insights(df, yearly_df, anomaly_years):
    insights = []

    if not yearly_df.empty:
        first_temp = yearly_df["temperature"].iloc[0]
        last_temp = yearly_df["temperature"].iloc[-1]
        temp_change = round(last_temp - first_temp, 2)

        first_co2 = yearly_df["co2"].iloc[0]
        last_co2 = yearly_df["co2"].iloc[-1]
        co2_change = round(last_co2 - first_co2, 2)

        insights.append(f"Average temperature changed by {temp_change} °C across the observed timeline.")
        insights.append(f"Average CO₂ level changed by {co2_change} ppm across the observed timeline.")

    region_temp = df.groupby("region")["temperature"].mean().sort_values(ascending=False)
    if not region_temp.empty:
        hottest_region = region_temp.index[0]
        insights.append(f"{hottest_region} is the warmest region on average in the selected view.")

    rain_var = df.groupby("region")["rainfall"].std().sort_values(ascending=False)
    if not rain_var.empty:
        most_variable_rain = rain_var.index[0]
        insights.append(f"{most_variable_rain} shows the highest rainfall variability.")

    if not anomaly_years.empty:
        top_year = anomaly_years.iloc[0]["year"]
        top_count = anomaly_years.iloc[0]["anomaly_count"]
        insights.append(f"The highest anomaly concentration was observed in {top_year} with {top_count} flagged records.")

    return insights