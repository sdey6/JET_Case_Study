-- checking html type tags in cleaned title
SELECT *
FROM {{ ref('stg_xkcd_comics') }}
WHERE title_cleaned LIKE '%<%' AND title_cleaned LIKE '%>%' AND title_cleaned LIKE '%/%'
