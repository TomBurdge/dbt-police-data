import json

import polars as pl
from functime.cross_validation import train_test_split
from functime.forecasting import (
    censored_model,
    naive,
    snaive,
)
from functime.metrics import smape
from functime.seasonality import add_calendar_effects, add_fourier_terms

# Load data
y = pl.read_parquet(
    "https://github.com/TracecatHQ/functime/raw/main/data/commodities.parquet"
)
entity_col, time_col = y.columns[:2]
X = y.select([entity_col, time_col]).pipe(add_calendar_effects(["month"])).collect()


y = (
    pl.scan_parquet("local/forces.parquet")
    .select(["force", "datetime"])
    .with_columns(pl.col("datetime").str.to_datetime().dt.truncate("1mo"))
    .group_by(["force", "datetime"])
    .count()
    .sort(by=["force", "datetime"])
)

all_months = y.select("datetime").unique().join(y.select("force").unique(), how="cross")
y = (
    all_months.join(y, how="left", on=["force", "datetime"])
    .sort(by=["force", "datetime"])
    .fill_null(strategy="forward")
    .select(["force", "datetime", "count"])
)
entity_col, time_col = y.columns[:2]
X = y.select([entity_col, time_col]).pipe(add_fourier_terms(sp=12, K=6)).collect()
test_size = 5
freq = "1mo"
y_train, y_test = train_test_split(test_size)(y)
X_train, X_test = train_test_split(test_size)(X)

# Paralleized naive forecasts!
y_pred_naive = naive(freq="1mo")(y=y_train, fh=3)
y_pred_snaive = snaive(freq="1mo", sp=12)(y=y_train, fh=3)
# Univariate time-series fit with automated lags and hyperparameter tuning
forecaster = censored_model(freq=freq, threshold=0.0, lags=3)(y=y_train, fh=3)
print(
    y.filter(pl.col("force") == "metropolitan")
    .sort(by="datetime", descending=True)
    .collect()
)
print(
    forecaster.filter(pl.col("force") == "metropolitan").sort(
        by="datetime", descending=True
    )
)
exit()
# Predict
y_pred = forecaster.predict(fh=test_size)
breakpoint()
# Score
scores = smape(y_true=y_test, y_pred=y_pred)
print("✅ Predictions (univariate):\n", y_pred.sort(entity_col))
print("💯 Scores (univariate):\n", scores.sort("smape"))
print("💯 Scores summary (univariate):\n", scores.select("smape").describe())

# Retrieve best lags and hyperparameters
best_params = forecaster.best_params
print(f"✨ Best parameters (y only):\n{json.dumps(best_params, indent=4)}")
breakpoint()
