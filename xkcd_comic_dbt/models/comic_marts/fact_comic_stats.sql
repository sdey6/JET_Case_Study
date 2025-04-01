-- Fact table fact_comic_stats

-- The fact_comic_stats table stores various metrics for further analysis. The below transformations are performed on this table-
-- 1.Calculating the title length for each comic.
-- 2.Calculating cost of each comic (title_length * 5) in Euros.
-- 3.View counts per comic is calculated by generating a random integer between 0 and 1 and multiplying that by 10000.
-- 4.Review score is computed by generating a random number between 1.0 and 10.0.
-- 5.A surrogate key stats_id is generated for future analysis per comic(how the review scores change/if views increase etc)
-- 6.Adds timestamp to indicate when all these metrics were generated.

-- calculation of views
-- In SQLite RANDOM() function returns a signed 64-bit integer ranging from -9223372036854775808 to +9223372036854775807
-- abs(random) gives a value between 0 to 9223372036854775807, then we normalize by 9223372036854775807.0 to scale from 0 to 1,
 --then rounding and casting to integer values.

-- calculation of reviews
--  In SQLite RANDOM() function returns a signed 64-bit integer ranging from -9223372036854775808 to +9223372036854775807. When we do
-- abs(random) all negative shifts to positive values and we get 0 to 9223372036854775807. Now if we normalize we get numbers from 0 to 1
-- by dividing by 9223372036854775807.0. Next the req is random numbers between 1 to 10 so multiply by 9 to get the range of 0 to 9 and add
-- 1 which shifts the range from 0->1 to 1->10. Then we round to clean. Casting is avoided to keep the float as per req.

{{ config(materialized='incremental', unique_key='comic_id') }}


WITH source_data AS (
    SELECT
        comic_id,
        title
    FROM {{ ref('dim_comic') }}
    {% if is_incremental() %}
        WHERE comic_id NOT IN (SELECT comic_id FROM {{ this }})
    {% endif %}
),
max_id AS (
    {% if is_incremental() %}
    SELECT COALESCE(MAX(stats_id), 0) AS current_max FROM {{ this }}
    {% else %}
    SELECT 0 AS current_max
    {% endif %}
),
final_output AS (
    SELECT
        max_id.current_max + ROW_NUMBER() OVER (ORDER BY comic_id) AS stats_id,
        comic_id,
        LENGTH(title) AS title_length,
        LENGTH(title) * 5 AS cost_eur,
        CAST(ROUND((ABS(RANDOM()) / 9223372036854775807.0) * 10000, 0) AS INTEGER) AS views,
        ROUND(1 + (ABS(RANDOM()) / 9223372036854775807.0) * 9, 1) AS review_score,
        CURRENT_TIMESTAMP AS created_at
    FROM source_data, max_id
)

SELECT * FROM final_output
