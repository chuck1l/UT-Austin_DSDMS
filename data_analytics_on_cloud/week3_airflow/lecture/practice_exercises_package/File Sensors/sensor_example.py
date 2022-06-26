# We'll start by importing the DAG object
from airflow import DAG
# We need to import the operators used in our tasks
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.dummy import DummyOperator
from datetime import timedelta, datetime

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

# Create the DAG object
with DAG(
    'sensor_example',
    default_args=default_args,
    description='Sensors Everywhere!',
    schedule_interval=None,
    catchup=False
) as dag:

    start = DummyOperator(
        task_id='start',
        dag=dag
    )

    file_sensor_1 = FileSensor(
        task_id='file_sensor_1',
        poke_interval=15,
        filepath='', # add path to folder 1
        timeout=60,
        dag=dag
    )

    file_sensor_2 = FileSensor(
        task_id='file_sensor_2',
        poke_interval=15,
        filepath='', # add path to folder 1
        timeout=60,
        dag=dag
    )

    file_sensor_3 = FileSensor(
        task_id='file_sensor_3',
        poke_interval=15,
        filepath='', # add path to folder 1
        timeout=60,
        dag=dag
    )

    process_data = DummyOperator(
        task_id='process_data',
        dag=dag
    )

    end = DummyOperator(
        task_id='end',
        dag=dag
    )

    start >> [file_sensor_1, file_sensor_2, file_sensor_3] >> process_data >> end