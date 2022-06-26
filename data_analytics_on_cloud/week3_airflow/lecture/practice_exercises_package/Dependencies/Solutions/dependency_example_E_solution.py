# Import Airflow and required operators
from lib2to3.pgen2.token import ENDMARKER
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
    'dependency_example_E',
    default_args=default_args,
    description='Practice Exercise 1[D]: Dummy Operator',
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

    task_4 = DummyOperator(
        task_id='task_4',
        dag=dag
    )

    task_5 = DummyOperator(
        task_id='task_5',
        dag=dag
    )

    task_6 = DummyOperator(
        task_id='task_6',
        dag=dag
    )

    task_7 = DummyOperator(
        task_id='task_7',
        dag=dag
    )

    task_8 = DummyOperator(
        task_id='task_8',
        dag=dag
    )

    task_9 = DummyOperator(
        task_id='task_9',
        dag=dag
    )

    task_10 = DummyOperator(
        task_id='task_10',
        dag=dag
    )

    task_11 = DummyOperator(
        task_id='task_11',
        dag=dag
    )

    start >> [task_1, task_2]
    task_2 >> [task_4, task_5] >> task_6
    task_5 >> [task_6, task_7] >> task_10 >> end
    task_1 >> task_3 >> task_8 >> task_9 >> task_11 >> end  