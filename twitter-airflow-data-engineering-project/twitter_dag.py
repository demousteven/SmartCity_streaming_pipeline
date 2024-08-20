from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from twitter_etl import run_twitter_etl

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',                      # The owner of the DAG
    'depends_on_past': False,                # Do not depend on past DAG runs
    'start_date': datetime(2020, 11, 8),    # The start date for the DAG; the first run will be on this date
    'email': ['airflow@example.com'],        # List of emails to notify on failure or retry
    'email_on_failure': False,               # Disable email notifications on task failure
    'email_on_retry': False,                 # Disable email notifications on task retry
    'retries': 1,                            # Number of retries in case of task failure
    'retry_delay': timedelta(minutes=1)      # Delay between retries
}

# Define the DAG
dag = DAG(
    'twitter_dag',                         # The unique identifier for the DAG
    default_args=default_args,             # Default arguments for the DAG
    description='Our first DAG with ETL process!',  # Description of the DAG
    schedule_interval=timedelta(days=1),  # The frequency at which the DAG should run (every day)
)

# Define the PythonOperator to execute the ETL process
run_etl = PythonOperator(
    task_id='complete_twitter_etl',      # Unique identifier for this task
    python_callable=run_twitter_etl,     # The Python function to be executed
    dag=dag,                            # The DAG to which this task belongs
)

# Set the task in the DAG (note: this line is optional if there is only one task)
run_etl
