# Libraries
from sqlalchemy import create_engine
import os
import pandas as pd
from dotenv import load_dotenv

# Load env variables (if you use a .env file)
load_dotenv()

# Main method of the loading process
def load_data(df):
    # Evironment variables to connect with database

    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    host = os.getenv("MYSQL_HOST")
    port = os.getenv("MYSQL_PORT")
    database = os.getenv("MYSQL_DATABASE")


    # Create the URL for MySQL with PyMySQL
    url = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'

    # Create engine
    engine = create_engine(url)
    print('\n✅ Successful connection to MySQL database')

    table_target = 'tb_nytimes_articles'

    # Load dataset to table
    df.to_sql(table_target, con=engine, if_exists='replace', index=False)
    print('\n✅ Table created and updated successfully')