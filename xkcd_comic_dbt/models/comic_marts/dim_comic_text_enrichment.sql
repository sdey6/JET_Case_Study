-- Dimension table dim_comic_text_enrichment
-- Table dim_comic_text_enrichment is created with below transformations. This table stores data for more text related analysis in future
-- 1. Selects comic textual metadata info like transcript, news etc from the staging model.
-- 2. Cleans empty string values from the text columns



{{ config(materialized='table') }}

WITH source_data AS (
SELECT * FROM {{ref('stg_xkcd_comics')}}
),
final_output AS (
    SELECT
    comic_id,
    NULLIF(TRIM(alt), '') AS alt, --clean empty string to null
    NULLIF(TRIM(transcript), '') AS transcript,
    NULLIF(TRIM(news), '') AS news,
    NULLIF(TRIM(link), '') AS link,
    CURRENT_TIMESTAMP AS created_at,
    CURRENT_TIMESTAMP AS modified_at
    FROM source_data
    WHERE comic_id IS NOT NULL
)
SELECT * FROM final_output
