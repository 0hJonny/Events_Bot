import os
import psycopg2
from PostgreSQL import *
from dotenv import load_dotenv

load_dotenv()

POSTGRES_DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL")
POSTGRES_DATABASE_NAME = os.getenv("POSTGRES_DATABASE_NAME")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_CONNECTION_PORT = os.getenv("POSTGRES_CONNECTION_PORT")

db_info = ("host='%s' \
        dbname='%s' \
        user='%s' \
        password='%s' \
        port='%s'"
           % (POSTGRES_DATABASE_URL,
              POSTGRES_DATABASE_NAME,
              POSTGRES_USERNAME,
              POSTGRES_PASSWORD,
              POSTGRES_CONNECTION_PORT))

connection = psycopg2.connect(db_info)


def initialize_database(cursor):
    cursor.execute(DB_INIT_TABLE_EVENTS)
