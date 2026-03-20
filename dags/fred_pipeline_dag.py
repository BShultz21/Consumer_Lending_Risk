from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from etl.fred_pipeline import load_api_data


with DAG(
        dag_id="consumer_lending_risk",
        start_date=datetime(2026, 3, 12),
        schedule="@weekly",
        catchup=False
):

    load_api_data = PythonOperator(
        task_id = "load_api_data",
        python_callable = load_api_data
    )


