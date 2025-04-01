# Data Quality Check Steps For XKCD Comic Data

The purpose of this document is to list down the necessary steps of data quality checking which ensures the integrity and quality of the data stored in the final data warehouse.
The checks for each table has been segregated below.
---

## dim_comic

- `comic_id` column should be unique as it's a primary key.
- `title` column should not be null.
- `date_id` column should not be null.
- `date_id` column should match a value in the `dim_date` table.

---

## dim_date

- `date_id` column should be unique as primary key.
- `date` column should not be null.
-  Checking if `year`, `month`, and `day` have valid calender values.

---

## dim_comic_text_enrichment

- Each row in the `comic_id` table should be present `dim_comic` table.
- At least one of four columns- `alt`, `transcript`, `news`, `link` should have a value.

---

## fact_comic_stats

- `stats_id` must be unique (primary key).
- `comic_id` should match a record in `dim_comic` table as it is foreign key to the table.
- `views` should be between 0 and 9999 inclusive based on the random number generation logic.
- `review_score` should be between 1.0 and 10.0 inclusive based on random number generation logic.
- `cost_eur` should be zero or greater.
- `loaded_at` should not be null.

---

These checks should be applied after loading and before using the data for analysis or reporting.
