-- Make sure  each enrichment row has at least one nonnull textual field, if all 4 are missing that would make that row almost useless
SELECT *
FROM {{ref('dim_comic_text_enrichment')}}
WHERE alt IS NULL
  AND transcript IS NULL
  AND news IS NULL
  AND link IS NULL
