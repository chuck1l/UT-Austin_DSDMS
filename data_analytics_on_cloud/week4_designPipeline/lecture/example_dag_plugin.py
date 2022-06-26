# Import Airflow and required operators
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator
# Import libraries to handle SQL and dataframes
import sqlalchemy as db
import pandas as pd
# Import libraries to keep time
from datetime import timedelta, datetime
# Import the variables and functions from config plugin
from config import database_ip, database_username, database_password, default_email, send_msg

# Create a SQL DB connection object
engine = db.create_engine(f'mysql+pymysql://{database_username}:{database_password}@{database_ip}:3306/mydb')

# Use the connection object to query and pull data

def fetch_count():
    with engine.connect() as connection:
        cursor = connection.execute(f"SELECT count(*) FROM sample_table")
        result = cursor.fetchall()[0][0]
    return result

default_args = {
    'owner': 'user_name',
    'start_date': datetime(2022, 2, 3),
    'depends_on_past': False,
    'email': [default_email],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

# Create the DAG object
with DAG(
    'example_dag_plugin',
    default_args=default_args,
    description='DAG with Plugins',
    schedule_interval=None,  # Replace None with */30 * * * * after testing
    catchup=False
) as dag:

    start_task = DummyOperator(
        task_id='start',
        dag=dag
    )

    end_task = DummyOperator(
        task_id='end',
        dag=dag
    )

    count_rows = PythonOperator(
        task_id='count_rows',
        python_callable=fetch_count,
        dag=dag
    )

    send_slack_message = PythonOperator(
    task_id='send_slack_message',
    python_callable=send_msg,
    op_kwargs={"text_string": "sample_table has rows"},
    dag=dag
    )

    start_task >> count_rows >> send_slack_message >> end_task






