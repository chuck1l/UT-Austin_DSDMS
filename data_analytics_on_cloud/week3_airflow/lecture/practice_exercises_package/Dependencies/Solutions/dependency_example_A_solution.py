# Import Airflow and required operators
from airflow import DAG
from airflow.operators.dummy import DummyOperator
# Import libraries to keep time
from datetime import timedelta, datetime

default_args = {
    'owner': 'user_name',
    'start_date': datetime(2022, 2, 3),
    'depends_on_past': False,
    'email':'airflow@gmail.com',
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

# Create the DAG object
with DAG(
    'dependency_example_A',
    default_args=default_args,
    description='Practice Exercise 1[A]: Dummy Operator',
    schedule_interval=None, 
    catchup=False
) as dag:

    start = DummyOperator(
        task_id='start',
        dag=dag
    )

    end = DummyOperator(
        task_id='end',
        dag=dag
    )
    
    task_1 = DummyOperator(
        task_id='task_1',
        dag=dag
    )

    task_2 = DummyOperator(
        task_id='task_2',
        dag=dag
    )

    task_3 = DummyOperator(
        task_id='task_3',
        dag=dag
    )

    start >> [task_1, task_2, task_3] >> end