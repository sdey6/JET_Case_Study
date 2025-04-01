-- staging table stg_xkcd_comics
-- Listing down all columns from the comics_staging_data for use by the other models

SELECT
    comic_id,
    month,
    link,
    year,
    news,
    safe_title,
    transcript,
    alt,
    img,
    title,
    day,
    created_at,
    updated_at
    FROM comics_staging_data