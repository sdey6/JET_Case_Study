FROM apache/airflow:2.7.2

# Make sure required system packages are installed
USER root
RUN apt-get update && apt-get install -y build-essential

# Switch back to airflow user
USER airflow

# Install matching DBT versions
RUN pip install "dbt-core==1.5.5" "dbt-sqlite==1.5.1"
