# Police Stop and Search Data.
This repo uses dbt, duckdb, and polars to download the latest stop and search data in the UK.

This project involves:
- Data I find interesting and important.
- An exploratory project on DBT.

Typically, as with this project, I like to explore tools such as DBT through *doing* after a very quick use of the example projects provided in documentation.

The dbt-duckdb plugin integrates well with python models, which is awesome.

Python is necessary for the initial API calls and downloads, but my aim is to create the transformation models with SQL. 

As a data engineer, it is easy to bias python. But well-written SQL is (arguably) more accessible, readable, and maintainable for teams with members who are relatively less technical.