# --------------------------------------------------
# Instructions on how to use this python file:
# --------------------------------------------------
"""
This file can do 3 things for you: 
[1] Add N number of rows in the zone_stats table
[2] Truncate/Delete all the rows of zone_stats, requirements & anomaly tables in SQLDB
[3] Keep added a stream of rows into zone_stats every N seconds

Have this file on the home directory of your cloud shell. Here are a few examples:
[1] python3 update_data.py --addrows=10
[2] python3 update_data.py --reset=1
[3] python3 update_data.py --interval=120
"""

# CHANGE THIS TO YOUR PATH BEFORE USING
FILE_PATH = "gs://pandemic-bucket/data/zone_stats.csv"

# Import necessary packages
import sqlalchemy as db
import pandas as pd
# Import argparse to accept arguments
import argparse
import time
import datetime

import warnings
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument('--interval', type=int, required=False, default=0)
parser.add_argument('--reset', type=int, required=False)
parser.add_argument('--addrows', type=int, required=False)
args = parser.parse_args()

# Set auth parameters
DATABASE_USERNAME = 'root'
DATABASE_PASSWORD = 'pandemic'
DATABASE_IP = '34.130.93.160'

# Create a SQL DB connection object
engine = db.create_engine(f'mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_IP}:3306/covid_db')

# If reset is True, clean the input data
if args.reset == 1:
    with engine.connect() as connection:
        connection.execute(f"TRUNCATE zone_stats;")
        connection.execute(f"TRUNCATE requirements;")
        connection.execute(f"TRUNCATE anomaly;")
elif args.interval != 0:
    # if not, append a row as per the interval
    df = pd.read_csv(FILE_PATH)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    for row in range(len(df)):
        with engine.connect() as connection:
            df.iloc[[row]].to_sql("zone_stats", engine, index=False, if_exists="append")
        print(row)
        time.sleep(args.interval)
else:
    df = pd.read_csv(FILE_PATH)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    with engine.connect() as connection:
        cursor = connection.execute("SELECT COUNT(*) FROM zone_stats")
        cnt = cursor.fetchall()[0][0]
    if cnt == 0: df = df.head(args.addrows)
    else:
        with engine.connect() as connection:
            cursor = connection.execute("SELECT MAX(timestamp) FROM zone_stats")
            max_time = cursor.fetchall()[0][0]
        df = df[df['timestamp'] > max_time].head(args.addrows)
    df.to_sql("zone_stats", engine, index=False, if_exists="append")