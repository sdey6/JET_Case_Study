# XKCD Comic ELT Project 

This project includes a data pipeline which extracts comic data from public XKCD API, then loads it in an SQLite database, 
transforms the data using `dbt`, also performs various data quality checks. All the processes are orchestrated Apache Airflow
running inside Docker.

---

## Main Features

- Extracts latest XKCD comics from XKCD API.
- Saves data into `comics_staging_data` table in SQLite DB.
- Runs dbt models to create a DWH structure including a staging table `stg_xkcd_comics` and facts and dimensions on top of it.
- Runs dbt tests on transformed data to ensure good data quality.
- The pipeline is dockerized and scheduled to run with Airflow every 15 minutes on **Mon, Wed and Fri**.

## Prerequisites

This project is designed to run via Docker for consistency and simplicity with Airflow.

### Tested Environment(Windows)

This project is developed and tested on Windows using Docker Desktop.

For windows (10/11)-
- [Docker Desktop][Docker Desktop](https://www.docker.com/products/docker-desktop)  
- [DB Browser for SQLite][DB Browser for SQLite](https://sqlitebrowser.org/) to inspect the DB (optional)

## Cloning Repo
```commandline
git clone https://github.com/sdey6/JET_Case_Study.git
cd JET_Case_Study
```


## Running the pipeline
1. Open Docker desktop and ensure its running.
2. In terminal-
```commandline
docker-compose up --build
```
3. After a few seconds go to http://localhost:8080
- Login details: userid- airflow pwd- airflow (default credentials as this is a non-production setup)
- Trigger the DAG `xkcd_comic_etl_dag`


## Running a Specific dbt Model or Test Manually (Optional)
To enter the container and run dbt manually
```commandline
docker exec -it jet_case_study-airflow-webserver-1 bash
```
Navigate to the dbt folder
```commandline
cd /opt/airflow/xkcd_comic_dbt
```

If to run a specific model

```bash
dbt run --select dim_comic --profiles-dir ./profiles
```

If to run test on a specific model
```bash
dbt test --select dim_comic --profiles-dir ./profiles
```


## A summary of the DWH

Overall this data warehouse follows a **Kimball star schema**.

Fact table:
fact_comic_stats: To store metrics like `title_length`, `cost_eur`, `views`, `review_score`, etc.

Dimensions table:
dim_comic: To store Base comic details like `comic_id`, `title` , `img` etc.

dim_comic_text_enrichment:To store additional comic information like `alt`, `transcript`, `news`

dim_date: This is a calendar dimension table generated from comic publication date

The ERD is provided in the docs folder under the JET_Case_Study

## Tasks
The DAG `xkcd_comic_etl_dag` has 3 tasks-

1. `xkcd_comic_etl_task`: Fetches comics from the XKCD API and loads into SQLite DB in a table.
2. `transformation_task`: Builds a staging table from the raw data and then runs all DBT models applying necessary transformation
3. `data_check_task`: Runs DBT tests to check the data quality

The DAG is Scheduled to run every 15 mins on Mon, Wed, Fri in a week.

The DAG execution order is extract → transform → check

## Future Scope
1. Extend setup to ensure smooth cross-platform support beyond Windows + Docker Desktop such as Ubuntu and Linux.
2. Using Postgres/ MySql database for data storage or cloud-based storage for DWH
3. Integrating alert systems for events
