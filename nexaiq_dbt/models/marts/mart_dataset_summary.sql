-- Mart model: Dataset summary statistics
-- This is the MART layer

{{ config(materialized='table') }}

WITH cleaned AS (
    SELECT * FROM {{ ref('stg_raw_data') }}
),

summary AS (
    SELECT
        org_id,
        dataset_id,
        COUNT(*) as total_rows,
        AVG(age) as avg_age,
        AVG(salary) as avg_salary,
        SUM(churn) as total_churned,
        ROUND(AVG(churn::numeric) * 100, 2) as churn_rate_pct
    FROM cleaned
    GROUP BY org_id, dataset_id
)

SELECT * FROM summary
