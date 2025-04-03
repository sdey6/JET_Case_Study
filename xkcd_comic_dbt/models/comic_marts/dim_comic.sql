-- dim_comic table
-- Table dim_comic is created with below transformations. This table stores important comic information.
-- 1. Selects comic metadata info like title, img etc from the staging model.
-- 2. Builds `date_id` col using the comics year, month and day and this will be a fkey to the dim_date table, this will give richer info about
--publication date of the comics
-- 3. Filters out comics with missing title.


{{ config(materialized='table') }}

WITH source_data AS
 (SELECT * FROM {{ ref('stg_xkcd_comics') }}),
final_output AS (
    SELECT
    comic_id,
    title_cleaned as title_cleaned,
    title_letter_count ,
    safe_title,
    img,
   CAST(year AS INTEGER) * 10000 --eg:20250000(the last 0000 is for mmdd
    + CAST(month AS INTEGER) * 100
    + CAST(day AS INTEGER) AS date_id,
    CURRENT_TIMESTAMP AS created_at,
    CURRENT_TIMESTAMP AS modified_at
    FROM source_data
    WHERE title_cleaned IS NOT NULL
)
SELECT * FROM final_output
