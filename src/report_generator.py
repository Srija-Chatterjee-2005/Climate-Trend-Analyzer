import os

def save_text_report(metrics, insights, output_path="outputs/reports/summary_report.txt"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    lines = [
        "Climate Trend Analyzer - Summary Report",
        "======================================",
        "",
        f"Average Temperature: {metrics['avg_temperature']} °C",
        f"Average Rainfall: {metrics['avg_rainfall']} mm",
        f"Average CO2: {metrics['avg_co2']} ppm",
        f"Average Sea Level: {metrics['avg_sea_level']} mm",
        f"Total Records: {metrics['records']}",
        "",
        "Key Insights:"
    ]

    for i, insight in enumerate(insights, start=1):
        lines.append(f"{i}. {insight}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Summary report saved at: {output_path}")