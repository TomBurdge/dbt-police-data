import polars as pl
from flaml import tune
from functime.cross_validation import train_test_split
from functime.forecasting import auto_lightgbm
from functime.seasonality import add_calendar_effects

# Load data
y = pl.read_parquet(
    "https://github.com/neocortexdb/functime/raw/main/data/commodities.parquet"
)
entity_col, time_col = y.columns[:2]
X = y.select([entity_col, time_col]).pipe(add_calendar_effects(["month"])).collect()

# Train-test splits
test_size = 3
freq = "1mo"
y_train, y_test = train_test_split(test_size)(y)
X_train, X_test = train_test_split(test_size)(X)


max_depth = 15
DEFAULT_TREE_DEPTH = 12

# Specify search space, initial conditions, and time budget
search_space = {
    "reg_alpha": tune.loguniform(1e-08, 10.0),
    "reg_lambda": tune.loguniform(1e-08, 10.0),
    "num_leaves": tune.randint(
        2, 2**max_depth if max_depth > 0 else 2**DEFAULT_TREE_DEPTH
    ),
    "colsample_bytree": tune.uniform(0.4, 1.0),
    "subsample": tune.uniform(0.4, 1.0),
    "subsample_freq": tune.randint(1, 7),
    "min_child_samples": tune.qlograndint(5, 100, 5),
}
points_to_evaluate = [
    {
        "num_leaves": 31,
        "colsample_bytree": 1.0,
        "subsample": 1.0,
        "min_child_samples": 20,
    }
]
time_budget = 420

# Fit model
forecaster = auto_lightgbm(
    freq="1mo",
    min_lags=20,
    max_lags=24,
    time_budget=time_budget,
    search_space=search_space,
    points_to_evaluate=points_to_evaluate,
)
forecaster.fit(y=y_train)

# Get best lags and model hyperparameters
best_params = forecaster.best_params
breakpoint()
