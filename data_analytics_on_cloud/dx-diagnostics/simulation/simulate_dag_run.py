# --------------------------------------------------
# Dx Diagnostics Simulation python file:
# --------------------------------------------------
"""
This code dumps a row into dx_data table in MySQL DB and then triggers the dx_diag_dags DAG on airflow
through a command. Then it waits for 60 seconds before the next iteration
"""

# CHANGE THE BELOW BEFORE RUNNING
FILE_PATH = './diag_metrics_P0015.csv'
ENVIRONMENT = 'dx-diagnostics-airflow'
LOCATION = 'us-central1'
DAG = 'dx_diag_dags'

# Imports to run commands on cloud shell
import os
import time
import pandas as pd

# Read the diagnostics csv
df = pd.read_csv(FILE_PATH)
os.system('python3 update_data.py --reset=1')

# Run dag for each row appended into the dx_data table
for i in range(len(df)):
    os.system('python3 update_data.py --addrows=1')
    os.system('gcloud composer environments run {} --location {} dags trigger -- {}'.format(ENVIRONMENT,LOCATION,DAG))
    time.sleep(60)