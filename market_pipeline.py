from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.append('C:\Python\sentinel-automation/scripts')
from scraper import run_scraper
from desktop_reporter import generate_desktop_report

default_args = {
    'owner': 'admin',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='market_sentinel_v1',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='0 3 * * *', # Roda todo dia às 03:00 AM
    catchup=False
) as dag:

    task_scrape = PythonOperator(
        task_id='scraping_concorrente',
        python_callable=run_scraper
    )

    task_report = PythonOperator(
        task_id='gerar_relatorio_desktop',
        python_callable=generate_desktop_report
    )

    task_scrape >> task_report # Define a ordem