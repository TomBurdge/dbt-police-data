{{ config(materialized='external',
location='s3://duckdb-stop-search-dev/forces.parquet'
)}}
SELECT *
FROM {{ ref("int_clean_wikipedia_forces")}}
