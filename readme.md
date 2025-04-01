# XKCD Comic ELT Project 

This project includes a data pipeline which extracts comic data from public XKCD API, then loads it in an SQLite database, 
transforms the data using `dbt`, also performs various data quality checks. All the processes are orchestrated Apache Airflow
running inside Docker.

---

## Main Features

- Extracts latest XKCD comics from XKCD API.
- Saves data into `comics_staging_data` table in SQLite DB.
- Runs dbt models to create a DWH structure including a staging table `stg_xkcd_comics` and facts and dimensions on top of it.
- Runs dbt tests on transformed data to ensure good data quality
- The pipeline is dockerized and scheduled to run with Airflow an every 15 minutes on **Mon, Wed and Fri**

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop)  This project is designed to run via Docker for consistency and simplicity with Airflow, hence a local non-Docker setup is not included.
- [DB Browser for SQLite](https://sqlitebrowser.org/) To inspect the DB (optional)

## Cloning the Repo
- If git is installed, type the below in terminal.
- git clone https://github.com/<your-username>/JET_Case_Study.git
- cd JET_Case_Study
- If git is not installed manually download the folder from github and extract.

## Running the pipeline
1. Open Docker desktop and ensure its running.
2. In terminal-
```bash
docker-compose up --build
```
3. After a few seconds go to http://localhost:8080
- Login details: userid- airflow pwd- airflow (default credentials as this is a non-production setup)
- Start the DAG `xkcd_comic_etl_dag`


## Running a Specific dbt Model or Test Manually
- Once the docker container is up (docker ps) and run below. This allows us to be inside the container where dbt is.
```bash
docker exec -it jet_case_study-airflow-webserver-1 bash
```
- Navigate to the dbt folder by below-
```bash
cd /opt/airflow/xkcd_comic_dbt
```

- If to run a specific model-

```bash
dbt run --select dim_comic --profiles-dir ./profiles
```

- If to run test on a specific model-
```bash
dbt test --select dim_comic --profiles-dir ./profiles
```


## A summary of the DWH

Overall this data warehouse follows a Kimball star schema.

Fact table:
fact_comic_stats: To store metrics like `title_length`, `cost_eur`, `views`, `review_score`, etc.

Dimensions table:
dim_comic: To store Base comic details like `comic_id`, `title` , `img` etc.

dim_comic_text_enrichment:To store additional comic information like `alt`, `transcript`, `news`

dim_date: This is a calendar dimension table generated from comic publication date



## Tasks
The DAG `xkcd_comic_etl_dag` has 3 tasks-

1. `xkcd_comic_etl_task`: Fetches comics from the XKCD API and loads into SQLite DB in a table.
2. `transformation_task`: Builds a staging table from the raw data and then runs all DBT models applying necessary transformation
3. `data_check_task`: Runs DBT tests to check the data quality

The DAG is Scheduled to run every 15 mins on Mon, Wed, Fri in a week.

The DAG execution order is extract → transform → check

