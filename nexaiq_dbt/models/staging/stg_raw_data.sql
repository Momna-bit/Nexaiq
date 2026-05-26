-- Staging model: Clean raw data
-- This is the CLEAN layer

{{ config(materialized='view') }}

SELECT
    org_id::text,
    dataset_id::text,
    COALESCE(age, 0) as age,
    COALESCE(salary, 0) as salary,
    COALESCE(churn, 0) as churn
FROM raw_data
WHERE org_id IS NOT NULL
  AND dataset_id IS NOT NULL
