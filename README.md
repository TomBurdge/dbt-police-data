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
