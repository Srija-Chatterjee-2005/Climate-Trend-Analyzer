import pandas as pd
from sklearn.linear_model import LinearRegression

def forecast_variable(df, variable="temperature", years_ahead=5):
    yearly = df.groupby("year")[variable].mean().reset_index()

    X = yearly[["year"]]
    y = yearly[variable]

    model = LinearRegression()
    model.fit(X, y)

    last_year = yearly["year"].max()
    future_years = pd.DataFrame({
        "year": list(range(last_year + 1, last_year + years_ahead + 1))
    })

    future_years[f"forecast_{variable}"] = model.predict(future_years[["year"]])

    return yearly, future_years