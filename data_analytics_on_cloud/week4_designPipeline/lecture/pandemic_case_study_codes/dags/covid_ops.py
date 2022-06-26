# Import Airflow Operators
from email.headerregistry import HeaderRegistry
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator
# Import libraries to handle SQL and dataframes
import pandas as pd
import numpy as np
# Import libraries to keep time
from datetime import timedelta, datetime
# Import functions from config
from config import send_msg, get_value_sql, get_rows_sql, append_row_sql, compute_zone_status

# --------------------------------
# Function Definitions
# --------------------------------
def get_remaining_patients(ti):
    """
    The patients who have not yet been discharged will add to the occupied beds when calculating it for the next hour.
    This function assumes that typically 30% of patients get discharged every hour and computes the remaining patients
    and passes this value on using Xcoms
    """
    # If you are checking this for the 1st record, it does not make sense
    count_rows = get_value_sql("SELECT COUNT(*) FROM zone_stats;")
    if count_rows == 1: 
        ti.xcom_push(key='remaining_patients',value=0)
    # From record 2 onwards, find the remaining patients and store the value using an Xcom
    else: 
        # Get the latest row's "need_hosp" value & compute the remaining according to the discharge rate
        need_hosp = get_value_sql("SELECT need_hosp FROM zone_stats WHERE timestamp = (select max(timestamp) from zone_stats);")
        rem_num = int(need_hosp - 0.3 * need_hosp)
        # Xcom to PUSH remaining patients
        ti.xcom_push(key='remaining_patients',value=rem_num)

def update_requirements(ti):
    """
    This function computes the requirements like beds available and oxygen supply remaining for each incoming
    record into the zones_stats table, and appends the results into the requirements table
    """
    # Read the latest record from the zone_stats table
    columns=['timestamp','zone_id','confirmed','deaths','recovered','tested','active','need_hosp','end_of_day']
    df = pd.DataFrame(get_rows_sql("SELECT * FROM zone_stats WHERE timestamp = (select max(timestamp) from zone_stats);"), columns=columns)
    # Create an temporary dataframe to update the requirements table
    temp = pd.DataFrame(columns=['timestamp','zone_id','beds_occupied','beds_available','beds_available_perc',
                                 'discharged','o2_consumed','o2_available','o2_available_perc'])
    temp['timestamp'] = pd.to_datetime(temp['timestamp'])
    # Requirement table updates
    temp['timestamp'] = df['timestamp']
    temp['zone_id'] = df['zone_id']
    temp['beds_occupied'] = df['need_hosp'] + ti.xcom_pull(key='remaining_patients',task_ids=['get_remaining_patients'])
    temp['beds_available'] = 1000 - temp['beds_occupied'] # Capacity of the care center is 1000
    temp['beds_available_perc'] = temp['beds_available'] / 1000
    temp['discharged'] = 0.3 * df['need_hosp'] # This is an assumption in this case study
    temp['o2_consumed'] = temp['beds_occupied'] * 2 * 6 * 60  # per person x 2 liters x per minute x avg 6 hrs hospitalization 
    temp['o2_available'] = 720000 - temp['o2_consumed'] + (50 * 2 * 6 * 60)  # o2 for 50 people replinished every hour
    temp['o2_available_perc'] = temp['o2_available'] / 720000
    # Append the row into the requirements SQL table
    append_row_sql(temp,'requirements')

def send_slack_notif():
    """
    Once the requirements table has been updated with the beds available and the o2 suppy remaining, 
    let's send this information out as a Slack Message
    """
    # Read the requirement table as a dataframe
    columns=['timestamp','zone_id','beds_occupied','beds_available','beds_available_perc','discharged','o2_consumed','o2_available','o2_available_perc']
    df = pd.DataFrame(get_rows_sql("SELECT * FROM requirements WHERE timestamp = (select max(timestamp) from zone_stats);"),columns=columns)
    # Get the values needed to part of the message
    time = str(df['timestamp'][0])
    beds_perc = round(df['beds_available_perc'][0]*100,2)
    o2_perc = round(df['o2_available_perc'][0]*100,2)
    # Send the slack message
    text_string = '{0}: {1} % of beds available and {2} % of oxygen supply remaining'.format(time, beds_perc,o2_perc)
    send_msg(text_string)

def aggregate_data():
    """
    At the end of every data, lets aggreagate the zone_stats table and find the average number of new cases we
    identified for the day and store it in a table which can be used to detect anomalies
    """
    # If its not the end of the day yet, skip this step
    eod = get_value_sql("SELECT end_of_day FROM zone_stats WHERE timestamp = (select max(timestamp) from zone_stats);")
    if eod == 0: pass
    # Else, aggregate the data for the day and store it in the anomaly table
    else: 
        columns=['timestamp','zone_id','avg_confirmed']
        df = pd.DataFrame(get_rows_sql("SELECT date(timestamp) as timestamp, zone_id, AVG(confirmed) avg_confirmed FROM zone_stats WHERE date(timestamp) = (select max(date(timestamp)) from zone_stats) group by 1,2;"), columns=columns)
        append_row_sql(df,'anomaly')

def send_zone_status():
    """
    Let's compute the status of the zone (GREEN, YELLOW, ORANGE, RED) at the end of the day and send the information
    out as a Slack Message
    """
    # If its not the end of the day yet, skip this step
    eod = get_value_sql("SELECT end_of_day FROM zone_stats WHERE timestamp = (select max(timestamp) from zone_stats);")
    if eod == 0: pass
    # Else, compute the zone status and send the message
    else:
        avg_con = eod = get_value_sql("SELECT avg_confirmed FROM anomaly WHERE timestamp = (select max(timestamp) from anomaly);")
        status = compute_zone_status(avg_con)
        text_string = 'Daily Zone Update: {} (average new cases: {})'.format(status, avg_con)
        send_msg(text_string)

# --------------------------------
# DAG definition
# --------------------------------
default_args = {
    'owner': 'user_name',
    'start_date': datetime(2022, 2, 3),
    'depends_on_past': False,
    'email': ['glsandbox98@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

# Create the DAG object
with DAG(
    'covid_ops',
    default_args=default_args,
    description='DAG with Plugins',
    schedule_interval=None,
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

    get_remaining_patients_task = PythonOperator(
        task_id='get_remaining_patients',
        python_callable=get_remaining_patients,
        dag=dag
    )

    update_requirements_task = PythonOperator(
        task_id='update_requirements',
        python_callable=update_requirements,
        dag=dag
    )

    aggregate_data_task = PythonOperator(
        task_id='aggregate_data',
        python_callable=aggregate_data,
        dag=dag
    )

    send_slack_notif_task = PythonOperator(
        task_id='send_slack_notif',
        python_callable=send_slack_notif,
        dag=dag
    )

    send_zone_status_task = PythonOperator(
        task_id='send_zone_status',
        python_callable=send_zone_status,
        dag=dag
    )

    # Set dependencies
    start_task >> get_remaining_patients_task >> update_requirements_task >> send_slack_notif_task
    send_slack_notif_task >> aggregate_data_task >> send_zone_status_task >> end_task