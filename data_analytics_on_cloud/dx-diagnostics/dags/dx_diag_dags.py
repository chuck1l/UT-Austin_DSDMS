# --------------------------------
# LIBRARIES
# --------------------------------

# Import Airflow Operators
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.sensors.file_sensor import FileSensor
# Import Libraries to handle dataframes
import csv
import pandas as pd
# Import Library to send Slack Messages
# Import Library toset DAG timing
from datetime import datetime
# Import functions from config
from config import send_msg, get_value_sql, get_rows_sql, append_row_sql

# --------------------------------
# CONSTANTS
# --------------------------------

# Set input and output paths
FILE_PATH_INPUT = '/home/airflow/gcs/data/input/'
FILE_PATH_OUTPUT_O2 = '/home/airflow/gcs/data/output/o2_anomaly_P0015.csv'
FILE_PATH_OUTPUT_HR = '/home/airflow/gcs/data/output/hr_anomaly_P0015.csv'

# --------------------------------
# Summary Statistics
# --------------------------------

# The Heart Rate and O2 Level Mean and Standard Deviation (mu and sigma accordingly)
hr_mu, hr_sigma = 80.81, 10.28
o2_mu, o2_sigma = 96.19, 1.69
# Hear Rate and O2 Level limits to exceed for anomaly
hr_limit = hr_mu + 3*hr_sigma
o2_limit = o2_mu + 3*o2_sigma

# --------------------------------
# FUNCTION DEFINITIONS
# --------------------------------

def update_results(id, ts, o2, hr, a_o2, a_hr, s_o2, s_hr, min_o2, min_hr, max_o2, max_hr):
    """
    This function computes the results; average, standard deviation, minimum and maximum for each incoming
    record into the dx_data table, and appends the results into the results table for long-term storage
    """
    # Initialize the column names
    cols=[
        'patient_id', 'timestamp', 'o2_level', 'heart_rate', 'avg_o2', 'avg_hr', 'std_o2', 'std_hr',
        'min_o2', 'min_hr', 'max_o2', 'max_hr'
    ]
    # Create an temporary dataframe to update the results table
    temp = pd.DataFrame(columns=cols)
    # Results table updates
    temp['patient_id'] = id
    temp['timestamp'] = pd.to_datetime(ts)
    temp['o2_level'] = o2
    temp['heart_rate'] = hr
    temp['avg_o2'] = a_o2
    temp['avg_hr'] = a_hr
    temp['std_o2'] = s_o2
    temp['std_hr'] = s_hr
    temp['min_o2'] = min_o2
    temp['min_hr'] = min_hr
    temp['max_o2'] = max_o2
    temp['max_hr'] = max_hr
    # Append the row into the requirements SQL table
    append_row_sql(temp,'diag_metrics')


# Function to filter anomalies in the data
# Add print statements to each output dataframe so that it appears on the Logs
def flag_anomaly():
    """
    As per the patient's past medical history, below are the mu and sigma 
    for normal levels of heart rate and o2:
    
    Heart Rate = (80.81, 10.28)
    O2 Level = (96.19, 1.69)

    Only consider the data points which exceed the (mu + 3*sigma) or (mu - 3*sigma) levels as anomalies
    Filter and save the anomalies as 2 dataframes in the output folder - hr_anomaly_P0015.csv & o2_anomaly_P0015.csv
    """
    # Source O2 Level Sample - Most Recent
    o2_measure = get_value_sql('SELECT o2_level FROM dx_data WHERE timestamp = (SELECT MAX(timestamp) FROM dx_data);')
    # Source Heart Rate Sample - Most Recent
    hr_measure = get_value_sql('SELECT heart_rate FROM dx_data WHERE timestamp = (SELECT MAX(timestamp) FROM dx_data);')
    # Source Patient ID - Most Recent
    patient_id = get_value_sql('SELECT patient_id FROM dx_data WHERE timestamp = (SELECT MAX(timestamp) FROM dx_data);')
    # Source timestamp - Most Recent
    timestamp = get_value_sql('SELECT timestamp FROM dx_data WHERE timestamp = (SELECT MAX(timestamp) FROM dx_data);')

    if hr_measure <= hr_limit:
        hr_status = 'GREEN, The Heart Rate measurement for the event is within limit'
    else:
        hr_status = 'RED, The Heart Rate measurement for the event is beyond 3-sigma limit'
        # Print for the logs
        print(
            '#####    ',
            patient_id, ': ', timestamp, ' ', hr_status,
            '    #####'
        )
        # Import the CSV, write the anomaly information, and save for Heart Rate exceeding event
        temp_hr_df = pd.read_csv(FILE_PATH_OUTPUT_HR)
        add_row_hr = {
            'patient_id':patient_id, 'timestamp':timestamp, 'heart_rate':hr_measure, 'status': hr_status
        }
        temp_hr_df = temp_hr_df.append(add_row_hr, ignore_index=True)
        temp_hr_df.to_csv(FILE_PATH_OUTPUT_HR, index=False)

    if o2_measure <= o2_limit:
        o2_status = 'GREEN, The Oxygen Level measurement for the event is within limit'
    else:
        o2_status = 'RED, The Oxygen Level measurement for the event is beyond 3-sigma limit'
        # Print for the logs
        print(
            '#####    ',
            patient_id, ': ', timestamp, ' ', o2_status,
            '    #####'
        )
        # Import the CSV, write the anomaly information, and save for O2 Level exceeding event
        temp_o2_df = pd.read_csv(FILE_PATH_OUTPUT_O2)
        add_row_o2 = {
            'patient_id':patient_id, 'timestamp':timestamp, 'o2_level':o2_measure, 'status': o2_status
        }
        temp_o2_df = temp_o2_df.append(add_row_o2, ignore_index=True)
        temp_o2_df.to_csv(FILE_PATH_OUTPUT_O2, index=False)

    return None


# Function to generate the diagnostics report
# Add print statements to each variable so that it appears on the Logs
def send_report():
    """
    This function sends a disgnostics report to Slack with
    the below patient details:
    #1. Average O2 level
    #2. Average Heart Rate
    #3. Standard Deviation of O2 level
    #4. Standard Deviation of Heart Rate
    #5. Minimum O2 level
    #6. Minimum Heart Rate
    #7. Maximum O2 level
    #8. Maximum Heart Rate
    """
    cols = ['patient_id', 'timestamp', 'o2_level', 'heart_rate']
    # Get all rows from the current table in gcs, create pandas DF
    df = pd.DataFrame(get_rows_sql('SELECT * FROM dx_data ORDER BY timestamp DESC'), columns=cols)
    # Patient ID, o2 sample, heart rate sample and most recent time
    patient = df.loc[0, 'patient_id']
    time = str(df.loc[0, 'timestamp'])
    o2_sample = df.loc[0, 'o2_level']
    hr_sample = df.loc[0, 'heart_rate']
    # Calculate the current average for both Heart Rate and O2 Level up to this point
    avg_o2 = round(df['o2_level'].mean(), 2)
    avg_hr = round(df['heart_rate'].mean(), 2)
    # Calculate the current Standard Deviation for both Heart Rate and O2 Level up to this point
    std_o2 = round(df['o2_level'].std(), 2)
    std_hr = round(df['heart_rate'].std(), 2)
    # Calculate the current Minimum reading for both Heart Rate and O2 Level up to this point
    min_o2 = df['o2_level'].min()
    min_hr = df['heart_rate'].min()
    # Calculate the current Maximum reading for both Heart Rate and O2 Level up to this point
    max_o2 = df['o2_level'].max()
    max_hr = df['heart_rate'].max()
    # Generate the text string that will be sent over SLACK messaging
    text_string_o2 = '{0}: patient {1} O2 Level metrics: Average {2}, Standard Dev {3}, Min {4}, Max {5}'.format(
        time, patient, avg_o2, std_o2, min_o2, max_o2)
    
    # Print these statistics for the logs every iteration
    print('\n')
    print(f'#####    O2 Level - Log: {text_string_o2}    #####')
    
    text_string_hr = '{0}: patient {1} Heart Rate metrics: Average {2}, Standard Dev {3}, Min {4}, Max {5}'.format(
        time, patient, avg_hr, std_hr, min_hr, max_hr)

    print(f'#####    Heart Rate - Log: {text_string_hr}    #####')
    print('\n')

    # Send Via Slack every 15 minutes
    time_stamp = pd.to_datetime(time)
    time_stamp = time_stamp.minute
    # Send the message if and only if the minute in the time stamp is evenly divisible by 15 (every 15 minutes) 
    # and it isn't the first two entries (at minute 0 for both 30 second entries), then for only the first of each 30
    if time_stamp % 15 == 0 and df.shape[0] > 2 and df.shape[0] % 2 == 0:
        # Send message 1 O2 Level metrics via slack on 15 minute intervals
        send_msg(text_string_o2)
        # Send message 2 Heart Rate mextrics via slack on 15 minute intervals
        send_msg(text_string_hr)
    # update the results table for long-term storage
    update_results(
        patient, time, o2_sample, hr_sample, avg_o2, avg_hr, std_o2, std_hr, min_o2, min_hr, max_o2, max_hr 
    )

    return None

# --------------------------------
# DAG definition
# --------------------------------

# Define the defualt args
default_args = {
    'owner': 'dx-diagnostics-airflow',
    'start_date': datetime(2022, 5, 8),
    'depends_on_past': False,
    'email': ['yzfr6_00@hotmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}
# Create the DAG object
with DAG(
    'dx_diag_dags',
    default_args=default_args,
    description='DAG with Plugins',
    schedule_interval=None,
    catchup=False
) as dag:
    # Start and End dubby operators
    start_task = DummyOperator(
        task_id='start_task',
        dag=dag
    )

    end_task = DummyOperator(
        task_id='end_task',
        dag=dag
    )
    # File sensor task
    file_sensor_task = FileSensor(
        task_id='file_sensor_task',
        poke_interval=30,
        filepath=FILE_PATH_INPUT,
        timeout=15,
        dag=dag
    )
    # Send report function writes to logs, updates the long-term storage, and sends the report if/when
    send_report_task = PythonOperator(
        task_id='send_report_task',
        python_callable=send_report,
        dag=dag
    )
    # Flags anomalies and writes them to the associated CSV files for output
    flag_anomaly_task = PythonOperator(
        task_id='flag_anomaly_task',
        python_callable=flag_anomaly,
        dag=dag
    )

    # Set dependencies
    start_task >> file_sensor_task
    file_sensor_task >> send_report_task >> end_task
    file_sensor_task >> flag_anomaly_task >> end_task
