# Import necessary packages
import sqlalchemy as db
import pandas as pd

# Set auth parameters
DATABASE_USERNAME = 'root'
DATABASE_PASSWORD = 'mysql101'
DATABASE_IP = '104.155.130.104' # This will change as per your external IP in GCP

# Create a SQL DB connection object
engine = db.create_engine(f'mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_IP}:3306/mydb')

# Use the connection object to query and pull data
with engine.connect() as connection:
    cursor = connection.execute(f"SELECT * FROM sample_table")
    result = cursor.fetchall()

df = pd.DataFrame(result)
print(df)
df.to_csv('sample_data.csv', index=None)