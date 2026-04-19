from src.data_generator import generate_climate_data
from src.data_preprocessing import load_data, preprocess_data
from src.analysis import (
    summary_metrics,
    yearly_trends,
    seasonal_analysis,
    region_comparison,
    decade_comparison,
    detect_anomalies,
    top_anomaly_years,
    correlation_table
)
from src.forecasting import forecast_variable
from src.insights import generate_insights
from src.report_generator import save_text_report
from src.utils import ensure_directories, save_line_chart

def run_pipeline():
    ensure_directories()

    generate_climate_data()
    df = load_data()
    df = preprocess_data(df)

    metrics = summary_metrics(df)
    yearly = yearly_trends(df)
    seasonal = seasonal_analysis(df)
    region_stats = region_comparison(df)
    decade_stats = decade_comparison(df)
    anomalies = detect_anomalies(df, column="temperature", threshold=2.0)
    anomaly_years = top_anomaly_years(df, column="temperature", threshold=2.0)
    corr = correlation_table(df)
    historical_temp, forecast_temp = forecast_variable(df, variable="temperature", years_ahead=5)

    insights = generate_insights(df, yearly, anomaly_years)

    yearly.to_csv("outputs/tables/yearly_trends.csv", index=False)
    seasonal.to_csv("outputs/tables/seasonal_analysis.csv", index=False)
    region_stats.to_csv("outputs/tables/region_comparison.csv", index=False)
    decade_stats.to_csv("outputs/tables/decade_comparison.csv", index=False)
    anomalies.to_csv("outputs/tables/anomalies.csv", index=False)
    anomaly_years.to_csv("outputs/tables/top_anomaly_years.csv", index=False)
    corr.to_csv("outputs/tables/correlation_matrix.csv")
    forecast_temp.to_csv("outputs/tables/temperature_forecast.csv", index=False)

    save_line_chart(
        yearly["year"], yearly["temperature"],
        "Yearly Temperature Trend", "Year", "Temperature (°C)",
        "outputs/charts/temperature_trend.png"
    )

    save_line_chart(
        yearly["year"], yearly["rainfall"],
        "Yearly Rainfall Trend", "Year", "Rainfall (mm)",
        "outputs/charts/rainfall_trend.png"
    )

    save_text_report(metrics, insights)

    print("Climate Trend Analyzer pipeline completed successfully.")

if __name__ == "__main__":
    run_pipeline()