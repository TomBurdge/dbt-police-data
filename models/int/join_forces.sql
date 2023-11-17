{{ config(materialized='external', location='file.parquet') }}
WITH forces AS (
  SELECT
    "Area of responsibility",
    REGEXP_REPLACE("Number of police officers"[2:], '\\[\\d\\]', '') AS number_officers,
    REGEXP_REPLACE("Budget (millions)"[2:], '\\[\\d\\]', '') AS "Budget (millions)",
    "Area Size (km2)",
    "Formed",
    "Legal jurisdiction",
    "Type",
    LOWER(REGEXP_REPLACE(Force, '( Police| Force| Constabulary| Service)$', '')) AS force
  FROM {{ ref("stg_wikipedia__forces") }}
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
    date_trunc('month', stop_searches.datetime) AS month
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
