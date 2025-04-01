
-- to test the year range in the dim_date table, should not be > current year
SELECT * FROM {{ref('dim_date')}}
WHERE year > CAST(strftime('%Y', 'now') AS INTEGER)
