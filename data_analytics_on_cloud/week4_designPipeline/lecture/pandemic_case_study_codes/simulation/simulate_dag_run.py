# --------------------------------------------------
# Instructions on how to use this python file:
# --------------------------------------------------
"""
This code dumps a row into zone_stats table in MySQL DB and then triggers the covid_ops DAG on airflow
through a command. Then it waits for 60 seconds before the next iteration
"""

# CHANGE THE BELOW BEFORE RUNNING
FILE_PATH = "gs://asia-east2-myairflowenv-2f8a5502-bucket/data/input/zone_stats.csv"
ENVIRONMENT = 'myairflowenv'
LOCATION = 'asia-east2'
DAG = 'covid_ops'

# Imports to run commands on cloud shell
import os
import time
import pandas as pd

# Read the zone_stats csv
df = pd.read_csv(FILE_PATH)
os.system('python3 update_data.py --reset=1')

# Run dag for each row appended into the zone_stats table
for i in range(len(df)):
    os.system('python3 update_data.py --addrows=1')
    os.system('gcloud composer environments run {} --location {} dags trigger -- {}'.format(ENVIRONMENT,LOCATION,DAG))
    time.sleep(60)