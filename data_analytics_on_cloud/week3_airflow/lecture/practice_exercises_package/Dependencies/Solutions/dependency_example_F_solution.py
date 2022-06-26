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
    'dependency_example_F',
    default_args=default_args,
    description='Practice Exercise 1[F]: Dummy Operator w/ more loops!!!',
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

    task_dict_layer_1 = {}
    
    for i in range(1,3):
        task_name = 'task_layer_1_' + str(i)
        task_dict_layer_1[task_name] = DummyOperator(
            task_id=task_name,
            dag=dag
        )

    task_dict_layer_2 = {}
    
    for j in range(1,4):
        task_name = 'task_layer_2_' + str(j)
        task_dict_layer_2[task_name] = DummyOperator(
            task_id=task_name,
            dag=dag
        )

    task_dict_layer_3 = {}
    
    for k in range(1,5):
        task_name = 'task_layer_3_' + str(k)
        task_dict_layer_3[task_name] = DummyOperator(
            task_id=task_name,
            dag=dag
        )
    
    for i in task_dict_layer_1:
        for j in task_dict_layer_2:
            start >> task_dict_layer_1[i] >> task_dict_layer_2[j]

    for j in task_dict_layer_2:
        for k in task_dict_layer_3:
            task_dict_layer_2[j] >> task_dict_layer_3[k] >> end
