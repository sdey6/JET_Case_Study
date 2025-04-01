import sys
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

sys.path.append("/opt/airflow")

from scripts.main import run_xkcd_process

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
}

DBT_PROJECT_PATH = "/opt/airflow/xkcd_comic_dbt"
PROFILE_DIR = os.path.join(DBT_PROJECT_PATH, "profiles")

with DAG(
        dag_id='xkcd_comic_etl_dag',
        description='The DAG polls XKCD comics every 15 minutes on Mon, Wed and Fri and inserts new comics if '
                    'available from the XKCD API.',
        default_args=default_args,
        start_date=datetime(2024, 3, 1),
        schedule_interval='*/15 * * * 1,3,5',  # Mon, Wed, Fri
        catchup=False
) as dag:
    # for inserting new comic
    run_data_load = PythonOperator(
        task_id='xkcd_comic_etl_task',
        python_callable=run_xkcd_process
    )
    # to run dbt transformations on the comics
    run_dbt_model = BashOperator(
        task_id='transformation_task',
        bash_command=f'cd {DBT_PROJECT_PATH} && dbt run --profiles-dir {PROFILE_DIR}'
    )

    # to test the data
    run_dbt_test = BashOperator(
        task_id='data_check_task',
        bash_command=f'cd {DBT_PROJECT_PATH} && dbt test --profiles-dir {PROFILE_DIR}'
    )

    # execution order
    run_data_load >> run_dbt_model >> run_dbt_test
