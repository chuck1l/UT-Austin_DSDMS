# Import the required libraries
from airflow import DAG
from airflow.operators import BashOperator, DummyOperator
from datetime import datetime, timedelta

# Initialize default arguments
default_args = {
    'owner':'user_name',
    'start_date':datetime(2022, 2, 3),
    'depends_on_past':False,
    'email':['glsandbox98@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=10)
}
 
# Create the DAG object
dag = DAG(
    'example_dag_01',
    default_args=default_args,
    description='My first Airflow DAG!',
    schedule_interval='*/5 * * * *',
    catchup=False
)
 
# Create the Task objects
start_task = DummyOperator(
    task_id='start',
    dag=dag
)

end_task = DummyOperator(
    task_id='end',
    dag=dag
)

hello_task = BashOperator(
    task_id='print_hello',
    bash_command='echo hello',
    dag=dag
)
 
world_task = BashOperator(
    task_id='print_world',
    bash_command='echo world',
    dag=dag
)
 
# Set dependency
start_task >> hello_task >> world_task >> end_task

# gcloud composer environments storage dags import --environment=myairflowenv --location=asia-east2 --source=example_dag_01.py