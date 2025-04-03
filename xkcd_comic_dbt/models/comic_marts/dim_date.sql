-- Table creation of dim_date with below transformation

-- Extracts distinct year,month and date from the staging model
-- Constructs valid full date values like yy-mm-dd
-- Generates date_id values like YYMMDD which acts as a PKey of the table
-- convert the data type of the columns like day,month and year from text to int
-- We also derive other attributes like weekday and week_number
-- This table can be used across the entire DWH for date related analysis

{{config(materialized='table')}}

WITH dates_stg AS(
    SELECT DISTINCT
    CAST(year AS INTEGER) AS year, --datatype conversion
    CAST(month AS INTEGER) AS month,
    CAST(day AS INTEGER) AS day
    FROM {{ref('stg_xkcd_comics')}}
    WHERE year IS NOT NULL AND month IS NOT NULL AND day IS NOT NULL
),
dates_formatted AS(
    SELECT year, month,day,
    DATE(year||'-'||printf('%02d', month)||'-'||printf('%02d', day)) AS valid_date --format into yy-mm-dd
    FROM dates_stg
)
SELECT --final query made from the above two subqueries
    CAST(STRFTIME('%Y%m%d', valid_date) AS INTEGER) AS date_id, --format as yymmdd
    valid_date AS date,
    year,
    month,
    day,
    STRFTIME('%w', valid_date) AS weekday,
    STRFTIME('%W', valid_date) AS week_number
    FROM dates_formatted
