import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.data_preprocessing import load_data, preprocess_data, data_quality_summary
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

st.set_page_config(page_title="Climate Trend Analyzer", layout="wide")

# ---------------- Custom UI ----------------
st.markdown("""
<style>

/* ========== PAGE BACKGROUND ========== */
.stApp {
    background: linear-gradient(135deg, #edf6f1 0%, #dcefe5 45%, #c7e6d5 100%);
    color: #123524;
}

/* Main container spacing */
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 95%;
}

/* ========== GLOBAL TEXT ========== */
html, body, p, span, label, div {
    color: #173b2f !important;
    font-family: "Segoe UI", sans-serif;
}

/* ========== TITLES ========== */
h1 {
    color: #0b3d2e !important;
    font-weight: 800 !important;
    letter-spacing: 0.3px;
}

h2, h3 {
    color: #184d3b !important;
    font-weight: 700 !important;
}

.small-note {
    color: #2f5d50 !important;
    font-size: 17px;
    font-weight: 600;
    margin-bottom: 0.6rem;
}

/* ========== SIDEBAR ========== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #163d31 0%, #1f6f5f 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

[data-testid="stSidebar"] .stMultiSelect div,
[data-testid="stSidebar"] .stSelectbox div,
[data-testid="stSidebar"] .stSlider div {
    color: #ffffff !important;
}

/* ========== INPUT BOXES IN SIDEBAR ========== */
[data-testid="stSidebar"] [data-baseweb="select"],
[data-testid="stSidebar"] [data-baseweb="tag"],
[data-testid="stSidebar"] .stSlider {
    border-radius: 14px;
}

/* ========== KPI / METRIC CARDS ========== */
[data-testid="metric-container"] {
    background: rgba(255, 255, 255, 0.72) !important;
    border: 1px solid rgba(255,255,255,0.45);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 18px 16px !important;
    box-shadow: 0 8px 24px rgba(27, 67, 50, 0.10);
    transition: all 0.3s ease;
}

/* Metric label */
[data-testid="metric-container"] label {
    color: #426b5f !important;
    font-size: 14px !important;
    font-weight: 700 !important;
}

/* Metric value */
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #102a22 !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
}

/* Optional delta hidden if unused */
[data-testid="stMetricDelta"] {
    color: #2a9d8f !important;
}

/* ========== TABS ========== */
button[data-baseweb="tab"] {
    background: rgba(255,255,255,0.45) !important;
    border-radius: 12px 12px 0 0 !important;
    margin-right: 6px !important;
    padding: 10px 18px !important;
    color: #2b5b4d !important;
    font-weight: 700 !important;
    border: none !important;
}

button[data-baseweb="tab"]:hover {
    background: rgba(255,255,255,0.75) !important;
    color: #163d31 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background: rgba(255,255,255,0.92) !important;
    color: #e76f51 !important;
    border-bottom: 3px solid #e76f51 !important;
}

/* ========== DATAFRAMES / TABLES ========== */
.stDataFrame, .stTable {
    background: rgba(255,255,255,0.82) !important;
    border-radius: 16px !important;
    padding: 8px !important;
}

/* ========== BUTTONS ========== */
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, #1b4332 0%, #2a9d8f 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.6rem 1rem !important;
    font-weight: 700 !important;
    box-shadow: 0 6px 16px rgba(27, 67, 50, 0.18);
}

.stButton > button:hover, .stDownloadButton > button:hover {
    background: linear-gradient(135deg, #16382a 0%, #21867b 100%) !important;
    color: white !important;
}

/* ========== INSIGHT CARDS ========== */
.insight-box {
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(255,255,255,0.5);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-left: 6px solid #2a9d8f;
    color: #173b2f !important;
    padding: 14px 16px;
    border-radius: 16px;
    margin-bottom: 12px;
    box-shadow: 0 8px 20px rgba(27, 67, 50, 0.08);
    font-weight: 600;
}

/* ========== SECTION SPACING ========== */
hr {
    border: none;
    height: 1px;
    background: rgba(23, 59, 47, 0.12);
    margin: 1rem 0;
}

/* ========== PLOTLY CONTAINER LOOK ========== */
.js-plotly-plot, .plot-container {
    border-radius: 18px !important;
    overflow: hidden !important;
}

/* ========== EXPANDERS IF USED LATER ========== */
.streamlit-expanderHeader {
    color: #184d3b !important;
    font-weight: 700 !important;
}

/* ========== SCROLLBAR (OPTIONAL POLISH) ========== */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #dcefe5;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: #86b9a2;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #5c9d84;
}

</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🌍 Climate Trend Analyzer</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='small-note'>Environmental Intelligence Dashboard for Trend Analysis, Seasonal Shifts, Anomaly Detection, and Forecasting</div>",
    unsafe_allow_html=True
)
st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- Load Data ----------------
df = load_data()
df = preprocess_data(df)

# ---------------- Sidebar ----------------
st.sidebar.header("🔎 Dashboard Controls")

regions = st.sidebar.multiselect(
    "Select Region(s)",
    options=sorted(df["region"].unique()),
    default=sorted(df["region"].unique())
)

year_min = int(df["year"].min())
year_max = int(df["year"].max())

year_range = st.sidebar.slider(
    "Select Year Range",
    year_min, year_max, (year_min, year_max)
)

season_filter = st.sidebar.multiselect(
    "Select Season(s)",
    options=["Winter", "Spring", "Summer", "Autumn"],
    default=["Winter", "Spring", "Summer", "Autumn"]
)

variable = st.sidebar.selectbox(
    "Select Climate Variable for Forecast/Anomaly",
    ["temperature", "rainfall", "co2", "sea_level"]
)

anomaly_threshold = st.sidebar.slider(
    "Anomaly Threshold (Z-score)",
    1.0, 3.5, 2.0, 0.1
)

forecast_horizon = st.sidebar.slider(
    "Forecast Horizon (Years)",
    1, 10, 5
)

filtered_df = df[
    (df["region"].isin(regions)) &
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1]) &
    (df["season"].isin(season_filter))
]

metrics = summary_metrics(filtered_df)
yearly = yearly_trends(filtered_df)
seasonal = seasonal_analysis(filtered_df)
region_stats = region_comparison(filtered_df)
decade_stats = decade_comparison(filtered_df)
anomalies = detect_anomalies(filtered_df, column=variable, threshold=anomaly_threshold)
anomaly_years = top_anomaly_years(filtered_df, column=variable, threshold=anomaly_threshold)
corr = correlation_table(filtered_df)
historical, forecast_df = forecast_variable(filtered_df, variable=variable, years_ahead=forecast_horizon)
quality = data_quality_summary(filtered_df)
insights = generate_insights(filtered_df, yearly, anomaly_years)

# ---------------- KPI Row ----------------
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("🌡 Avg Temp", f"{metrics['avg_temperature']} °C")
c2.metric("🌧 Avg Rainfall", f"{metrics['avg_rainfall']} mm")
c3.metric("🏭 Avg CO₂", f"{metrics['avg_co2']} ppm")
c4.metric("🌊 Avg Sea Level", f"{metrics['avg_sea_level']} mm")
c5.metric("📦 Records", f"{metrics['records']}")

# ---------------- Tabs ----------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Overview",
    "Time Trends",
    "Seasonal View",
    "Region Comparison",
    "Anomalies",
    "Forecast",
    "Insights",
    "Data Quality"
])

# ---------------- Tab 1 ----------------
with tab1:
    st.subheader("Overview Dashboard")

    fig_overview = px.line(
        yearly,
        x="year",
        y=["temperature", "rainfall", "co2", "sea_level"],
        title="Climate Indicators Over Time"
    )
    st.plotly_chart(fig_overview, use_container_width=True)

    st.subheader("Dataset Preview")
    st.dataframe(filtered_df.head(25), use_container_width=True)

# ---------------- Tab 2 ----------------
with tab2:
    st.subheader("Time Trend Analysis")

    fig_temp = px.line(yearly, x="year", y="temperature", markers=True, title="Yearly Temperature Trend")
    fig_temp.update_layout(template="plotly_white")
    st.plotly_chart(fig_temp, use_container_width=True)

    fig_rain = px.area(yearly, x="year", y="rainfall", title="Yearly Rainfall Trend")
    st.plotly_chart(fig_rain, use_container_width=True)

    fig_co2 = px.line(yearly, x="year", y="co2", markers=True, title="Yearly CO₂ Trend")
    st.plotly_chart(fig_co2, use_container_width=True)

    fig_sea = px.line(yearly, x="year", y="sea_level", markers=True, title="Yearly Sea Level Trend")
    st.plotly_chart(fig_sea, use_container_width=True)

    st.subheader("Decade Comparison")
    fig_decade = px.bar(
        decade_stats,
        x="decade",
        y=["temperature", "rainfall", "co2", "sea_level"],
        barmode="group",
        title="Decade-wise Climate Comparison"
    )
    st.plotly_chart(fig_decade, use_container_width=True)

# ---------------- Tab 3 ----------------
with tab3:
    st.subheader("Seasonal Climate Patterns")

    fig_season_temp = px.bar(
        seasonal, x="season", y="temperature",
        title="Season-wise Temperature"
    )
    st.plotly_chart(fig_season_temp, use_container_width=True)

    fig_season_rain = px.bar(
        seasonal, x="season", y="rainfall",
        title="Season-wise Rainfall"
    )
    st.plotly_chart(fig_season_rain, use_container_width=True)

# ---------------- Tab 4 ----------------
with tab4:
    st.subheader("Region Comparison")

    fig_region_temp = px.bar(
        region_stats, x="region", y="temperature",
        title="Average Temperature by Region"
    )
    st.plotly_chart(fig_region_temp, use_container_width=True)

    fig_region_rain = px.bar(
        region_stats, x="region", y="rainfall",
        title="Average Rainfall by Region"
    )
    st.plotly_chart(fig_region_rain, use_container_width=True)

    fig_region_co2 = px.bar(
        region_stats, x="region", y="co2",
        title="Average CO₂ by Region"
    )
    st.plotly_chart(fig_region_co2, use_container_width=True)

# ---------------- Tab 5 ----------------
with tab5:
    st.subheader(f"Anomaly Detection for {variable.title()}")

    fig_anomaly = px.scatter(
        anomalies,
        x="date",
        y=variable,
        color="anomaly",
        hover_data=["region", "year", "season", "z_score"],
        title=f"{variable.title()} Anomaly Timeline"
    )
    st.plotly_chart(fig_anomaly, use_container_width=True)

    st.subheader("Top Anomaly Years")
    st.dataframe(anomaly_years, use_container_width=True)

    st.subheader("Flagged Anomaly Records")
    flagged = anomalies[anomalies["anomaly"] == True][["date", "region", variable, "z_score"]]
    st.dataframe(flagged.head(50), use_container_width=True)

# ---------------- Tab 6 ----------------
with tab6:
    st.subheader(f"{variable.title()} Forecast")

    fig_forecast = go.Figure()
    fig_forecast.add_trace(go.Scatter(
        x=historical["year"],
        y=historical[variable],
        mode="lines+markers",
        name="Historical"
    ))
    fig_forecast.add_trace(go.Scatter(
        x=forecast_df["year"],
        y=forecast_df[f"forecast_{variable}"],
        mode="lines+markers",
        name="Forecast"
    ))
    fig_forecast.update_layout(
        title=f"{variable.title()} Historical Trend and Forecast",
        xaxis_title="Year",
        yaxis_title=variable.title()
    )

    st.plotly_chart(fig_forecast, use_container_width=True)
    st.dataframe(forecast_df, use_container_width=True)

# ---------------- Tab 7 ----------------
with tab7:
    st.subheader("Automatically Generated Insights")
    for point in insights:
        st.markdown(f"<div class='insight-box'>✅ {point}</div>", unsafe_allow_html=True)

    st.subheader("Correlation Matrix")
    st.dataframe(corr, use_container_width=True)

    st.download_button(
        "⬇ Download Filtered Dataset as CSV",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_climate_data.csv",
        mime="text/csv"
    )

    st.download_button(
        "⬇ Download Forecast Table",
        data=forecast_df.to_csv(index=False).encode("utf-8"),
        file_name=f"{variable}_forecast.csv",
        mime="text/csv"
    )

# ---------------- Tab 8 ----------------
with tab8:
    st.subheader("Data Quality Summary")

    q1, q2, q3, q4, q5 = st.columns(5)
    q1.metric("Rows", quality["rows"])
    q2.metric("Columns", quality["columns"])
    q3.metric("Missing Values", quality["missing_values"])
    q4.metric("Duplicates", quality["duplicate_rows"])
    q5.metric("Regions", quality["regions"])

    st.subheader("Filtered Dataset Shape")
    st.write(filtered_df.shape)

    st.subheader("Statistical Summary")
    st.dataframe(filtered_df.describe(include="all"), use_container_width=True)