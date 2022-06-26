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

    task_dict_layer_1 = {} # Create an empty dictionary for layer 1   
    # Create key values in the dictionary for each task
    for i in range(1,3):
        task_name = 'task_layer_1_' + str(i)
        task_dict_layer_1[task_name] = DummyOperator(
            task_id=task_name,
            dag=dag
        )

    task_dict_layer_2 = {} # Create an empty dictionary for layer 2
    # Create key values in the dictionary for each task
    for j in range(1,4):
        task_name = 'task_layer_2_' + str(j)
        task_dict_layer_2[task_name] = DummyOperator(
            task_id=task_name,
            dag=dag
        )

    task_dict_layer_3 = {} # Create an empty dictionary for layer 3
    # Create key values in the dictionary for each task
    for k in range(1,5):
        task_name = 'task_layer_3_' + str(k)
        task_dict_layer_3[task_name] = DummyOperator(
            task_id=task_name,
            dag=dag
        )
    
    # Set Dependencies
    
    # Connect every layer 1 task with every layer 2 task (Hint: Use nested for loops and iterate through each dict element & set dependency)


    # ----------------------------------
    
    # Connect every layer 2 task with every layer 3 task (Hint: Use nested for loops and iterate through each dict element & set dependency)


    # ----------------------------------