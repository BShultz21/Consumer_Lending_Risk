from datetime import datetime
from airflow import DAG, task
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from etl.fred_pipeline import load_api_data


with DAG(
        dag_id="consumer_lending_risk",
        start_date=datetime(2026, 3, 12),
        schedule="@weekly",
        catchup=False
):

    """
    truncate_sql_table = SQLExecuteQueryOperator(
        task_id="truncate_sql_table",
        sql="TRUNCATE TABLE consumer_lending_risk;",
        conn_id="postgres",
    )
    """

    load_api_data = PythonOperator(
        task_id = "load_api_data",
        python_callable = load_api_data
    )


