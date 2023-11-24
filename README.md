# Police Stop and Search Data.
This repo uses dbt, duckdb, and polars to download the latest stop and search data in the UK.

This project involves:
- Data I find interesting and important.
- An exploratory project on DBT.

Typically, as with this project, I like to explore tools such as DBT through *doing* after a very quick use of the example projects provided in documentation.


## On Python

The dbt-duckdb plugin integrates well with python models, which is awesome.

Python is necessary for the initial API calls and downloads, but my aim is to create the transformation models with SQL.

As a data engineer, it is easy to bias python. But well-written SQL is (arguably) more accessible, readable, and maintainable for teams with members who are relatively less technical.

Alongside this, keeping compute and persisted tables in a data warehouse is very convenient with DBT.

When the use case and transformations are relatively simple, I aim to learn whether SQL with DBT is a better choice than python for ETL pipelines.

# WIP - the Concept
I am planning to run a very simple web app with streamlit, which illustrates information about stop and searches in the UK.

The data will update incrementally with a DBT pipeline.

If this were a professional project I would usually (though not always) set up a data pipeline with a data warehouse rather than DuckDB.

But my aim for this project is that the cloud compute cost is very low (<£2/month).

The plan is for the:
- dbt models to run periodically in a container.
- The mart models will be materialised as parquet on object storage.
- The streamlit will read the appropriate materialised tables from cloud storage.

Delta lake format or partitioned parquet overwrites would be great for the object storage, to allow better incremental loading, but the dbt-duckdb nor its delta lake plugin support the functionality that I need yet.
