{{ config(materialized='external', location='file.parquet') }}
SELECT *
FROM {{ ref("stg_wikipedia__forces")}}