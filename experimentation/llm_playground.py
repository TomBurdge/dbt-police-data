import polars as pl
from dotenv import load_dotenv
from functime.llm import LLMActions

load_dotenv()


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
    .select(["force", "datetime", "count"])
)

dataset_context = "This dataset comprises of stop and search incidents in the uk between 2020 to 2023."

llm = LLMActions(y.collect())

# woo , this works!
analysis = llm.analyze(context=dataset_context, basket=["metropolitan", "lancashire"])

breakpoint()
