# We'll start by importing the DAG object
from airflow import DAG
# We need to import the operators used in our tasks
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.sensors.file_sensor import FileSensor
from datetime import timedelta, datetime

# Import libraries to send email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Other imports to work with data
import pandas as pd
import os

# CONSTANTS
HOME_DIR = '/home/airflow/gcs/data'
FILE_PATH = HOME_DIR + '/current'
ARCHIVE_PATH = HOME_DIR + '/archive'

DEFAULT_EMAIL = "" # Add your burner Gmail ID here
DEFAULT_PASSWORD = "" 

def prepare_data():
    file_name = os.listdir(FILE_PATH)[0]
    file_number = [x for x in file_name if x.isdigit()][0]
    # Read the latest store data
    store_data = pd.read_csv(f"{FILE_PATH}/{file_name}")
    # Add file number
    store_data['file_number'] = file_number
    # Filter data for each store
    store_978_df = store_data[store_data['store_id'] == 978]
    store_649_df = store_data[store_data['store_id'] == 649]
    # Create a csv for each store and drop it into their folders
    store_978_df.to_csv(f"{HOME_DIR}/store_978/store_data_978_{file_number}.csv", index=False)
    store_649_df.to_csv(f"{HOME_DIR}/store_649/store_data_649_{file_number}.csv", index=False)
    # Clean the current folder to accept the next file when it arrives
    os.system(f'mv {FILE_PATH}/{file_name} {ARCHIVE_PATH}')

def send_email(sender, receiver, subject, body, file_path=None):
    # Create an instance of MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver 
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    if file_path: 
        # Open file to be attached
        attachment = open(file_path, "rb")
        # Prepare attachment and add to the message
        att = MIMEBase('application', 'octet-stream')
        att.set_payload((attachment).read())
        encoders.encode_base64(att)
        att.add_header('Content-Disposition', f"attachment; filename= {file_path}")
        msg.attach(att)
    # Create SMTP session and send the mail  
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(DEFAULT_EMAIL, DEFAULT_PASSWORD)
    text = msg.as_string()
    s.sendmail(sender, receiver, text)
    # Terminate the session
    s.quit()

def no_file():
    # Create an instance of MIMEMultipart
    body = "The latest store data has not been dumped into the current folder. Check if there are any upstream issues with data generation!"
    send_email(
        DEFAULT_EMAIL,
        'glsandbox98+team@gmail.com', # change this to your TO: email address
        "DELAY IN DATA ARRIVAL",
        body
    )

def send_update_email(store_id, mail_to):
    body = "PFA the additional inventory requirements for your store. If the file is empty, all inventory levels are satisfied."
    file_path = f'{HOME_DIR}/inventory/low_inv_store_{store_id}.csv'
    send_email(
        DEFAULT_EMAIL,
        f"glsandbox98+{store_id}@gmail.com", # change this to your TO: email address
        f"INVENTORY UPDATE FOR STORE {store_id}",
        body,
        file_path
    )

def check_inventory(store_id):
    file_path = f'{HOME_DIR}/store_{store_id}/'
    file_name = max(os.listdir(file_path))
    print(file_name)
    # Read the store data and the minimum inventory requirement data
    store_df = pd.read_csv(file_path + file_name)
    inv_df = pd.read_csv(f'{HOME_DIR}/inventory/min_inventory.csv')
    # Get all the categories where the requirment is not met
    store_inv_df = pd.merge(store_df, inv_df, 'inner')
    store_inv_df = store_inv_df[store_inv_df['inventory'] < store_inv_df['min_inventory']]
    store_inv_df = store_inv_df[['prod_cat_desc','inventory','min_inventory']]
    store_inv_df['additional_inventory'] = store_inv_df['min_inventory'] - store_inv_df['inventory']
    # Write into inventory folder with store_id in the path
    store_inv_df.to_csv(f'{HOME_DIR}/inventory/low_inv_store_{store_id}.csv', index=False)

# initializing the default arguments that we'll pass to our DAG
# Initialize default arguments
default_args = {
    'owner':'user_name',
    'start_date':datetime(2022, 2, 3),
    'depends_on_past':False,
    'email':[DEFAULT_EMAIL],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries':0
}

# Create the DAG object
with DAG(
    'store_ops',
    default_args=default_args,
    description='DAG to track the inventory levels in stores',
    schedule_interval=None, # Replace None with */30 * * * * after testing
    catchup=False
) as dag:

    start_task = DummyOperator(
        task_id='start',
        dag=dag
    )

    file_sensor = FileSensor(
        task_id='file_sensor', 
        poke_interval=15,
        filepath=FILE_PATH,
        timeout=45,
        dag=dag
    )

    end_task = DummyOperator(
        task_id='end',
        dag=dag
    )

    process_data = PythonOperator(
        task_id='process_data',
        python_callable=prepare_data,
        dag=dag
    )

    check_inventory_store_649 = PythonOperator(
        task_id='check_inventory_store_649',
        python_callable=check_inventory,
        op_kwargs={'store_id': '649'},
        dag=dag
    )

    check_inventory_store_978 = PythonOperator(
        task_id='check_inventory_store_978',
        python_callable=check_inventory,
        op_kwargs={'store_id': '978'},
        dag=dag
    )

    send_update_mail_649 = PythonOperator(
        task_id="send_update_mail_649",
        python_callable=send_update_email,
        op_kwargs={"store_id": "649", "mail_to": DEFAULT_EMAIL},
        dag=dag
    )

    send_update_mail_978 = PythonOperator(
        task_id="send_update_mail_978",
        python_callable=send_update_email,
        op_kwargs={"store_id": "978", "mail_to": DEFAULT_EMAIL},
        dag=dag
    )

    no_file_found = PythonOperator(
        task_id='no_file_found',
        python_callable=no_file,
        trigger_rule='all_failed',
        dag=dag
    )

    start_task >> file_sensor >> process_data >> [check_inventory_store_649,check_inventory_store_978]
    file_sensor >> no_file_found 
    check_inventory_store_649 >> send_update_mail_649
    check_inventory_store_978 >> send_update_mail_978
    [send_update_mail_649,send_update_mail_978] >> end_task
