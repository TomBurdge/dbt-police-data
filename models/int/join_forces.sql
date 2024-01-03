{{ config(materialized='external', location='forces.parquet') }}
WITH forces AS (
  SELECT
    "Area of responsibility",
    "Number of police officers" as number_officers,
    "Budget (millions)",
    "Area Size (km2)",
    "Formed",
    "Legal jurisdiction",
    "Type",
    Force AS force
  FROM {{ ref("int_clean_wikipedia_forces") }}
  ),
stop_searches_forces AS(
  SELECT
    forces."Area of responsibility",
    forces.number_officers,
    forces."Budget (millions)",
    forces."Area Size (km2)",
    forces."Formed",
    forces."Legal Jurisdiction",
    stop_searches.force AS force,
    month
  FROM {{ ref("stg_api__stop_search")}} AS stop_searches
  LEFT JOIN forces
  ON stop_searches.force = forces.force
)
SELECT
  "month",
  "force",
  COUNT(*) AS number_searches
FROM stop_searches_forces
GROUP BY "force", "month"
ORDER BY "force","month", number_searches
