# Import necessary Libraries for slack, sql and dataframes
import requests
import sqlalchemy as db
import pandas as pd

# --------------------------------------
# MySQL Database Constants
# --------------------------------------
database_ip = "34.130.93.160" # change this to your public ip
database_username = "root"
database_password = "pandemic"

# --------------------------------------
# Slack Messages
# --------------------------------------
# The slack webhook link will change as per the one generated for your app
slack_webhook = "https://hooks.slack.com/services/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"
# Function to send slack message
def send_msg(text_string): requests.post(slack_webhook, json={'text': text_string}) 

# --------------------------------------
# SQL Query Functions
# --------------------------------------
# Create connection to MySQL database
engine = db.create_engine(f'mysql+pymysql://{database_username}:{database_password}@{database_ip}:3306/covid_db')
# Function to fetch rows from a SQL table and return it as a dataframe
def get_rows_sql(query):
    with engine.connect() as connection:
        cursor = connection.execute(query)
        result = cursor.fetchall()
    return result

# Function to fetch a value from a SQL table and return it
def get_value_sql(query):
    with engine.connect() as connection:
        cursor = connection.execute(query)
        val = cursor.fetchall()[0][0]
    return val

# Function to append a row into a SQL table
def append_row_sql(row,table):
    row.to_sql(table, engine, index=False, if_exists="append")

# --------------------------------------
# Function for flagging Anomalies
# --------------------------------------
def compute_zone_status(cases):
    """
    The assumption here is the mean of new cases reported 
    is around 250 and a deviation of 50 is tolerable
    """
    if cases <= 300: status = 'GREEN, average positive cases for the day are within limit'
    elif cases > 300 and cases <= 350: status = 'YELLOW, average positive cases for the day are beyond 1-sigma limit'
    elif cases > 350 and cases <= 400: status = 'ORANGE, average positive cases for the day are beyond 2-sigma limit'
    else: status = 'RED, average positive cases for the day are beyond 3-sigma limit'
    return status