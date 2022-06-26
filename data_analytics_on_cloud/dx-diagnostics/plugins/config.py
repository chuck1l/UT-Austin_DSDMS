# Import necessary Libraries for slack, sql and dataframes
import requests
import sqlalchemy as db
import pandas as pd

# --------------------------------------
# MySQL Database Constants
# --------------------------------------
database_ip = "34.133.227.79"
database_username = "root"
database_password = "root"

# --------------------------------------
# Slack Messages
# --------------------------------------
# Slack webhook link
slack_webhook = 'https://hooks.slack.com/services/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'

# Function to send slack message
def send_msg(text_string):
    requests.post(slack_webhook, json={'text': text_string}) 

# --------------------------------------
# SQL Query Functions
# --------------------------------------
# Create connection to MySQL database
engine = db.create_engine(f'mysql+pymysql://{database_username}:{database_password}@{database_ip}:3306/dx_diag_db')
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
