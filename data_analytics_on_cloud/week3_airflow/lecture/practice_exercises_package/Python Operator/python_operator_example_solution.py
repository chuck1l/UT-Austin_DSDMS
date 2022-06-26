# We'll start by importing the DAG object
from airflow import DAG
# We need to import the operators used in our tasks
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import timedelta, datetime
import statistics 

# initializing the default arguments that we'll pass to our DAG
# Initialize default arguments
default_args = {
    'owner': 'user_name',
    'start_date': datetime(2022, 2, 3),
    'depends_on_past': False,
    'email': 'airflow@gmail.com',
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

# Define a function to print the current date
def print_current_date():
    print("current datetime = {}".format(datetime.now()))

# Define a function to print the range of list of numbers
def get_max_num(lst):
    print("range of the list:{}".format(max(lst) - min(lst)))

# Define a function to print the mean and standard deviation of a list of numbers
def get_mean_stdev(lst):
    print("mean of the list:{}".format(statistics.mean(lst)))
    print("stdev of the list:{}".format(statistics.stdev(lst)))

# Create the DAG object
with DAG(
    'python_operator_example',
    default_args=default_args,
    description='Run user defined functions using PythonOperator',
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

    print_current_date_task = PythonOperator(
        task_id='print_current_date',
        python_callable=print_current_date,
        dag=dag
    )

    get_max_num_task = PythonOperator(
        task_id='get_max_num',
        python_callable=get_max_num,
        op_kwargs={'lst': [25,67,98,93,24,34]},
        dag=dag
    )

    get_mean_stdev_task = PythonOperator(
        task_id='get_mean_stdev',
        python_callable=get_mean_stdev,
        op_kwargs={'lst': [25,67,98,93,24,34]},
        dag=dag
    )

    start >> print_current_date_task >> get_max_num_task >> get_mean_stdev_task >> end