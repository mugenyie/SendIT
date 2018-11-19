import psycopg2
from pprint import pprint
from datetime import datetime
import urllib.parse as urlparse
from dotenv import load_dotenv
from urllib.parse import urlparse
from api.utils import encrypt_password
import os


class DatabaseConnection:
    try:
        def __init__(self):
            load_dotenv()
            database_uri = os.environ.get('DATABASE_URL')
            result = urlparse(database_uri)
            self.connection = psycopg2.connect(
                dbname=result.path[1:],
                user=result.username,
                password=result.password,
                host=result.hostname,
                port=result.port
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            pprint("Connected!")
    except:
        pprint("Failed To Connect to Database")

    def create_database_relations(self):
        create_tables_command = """
        CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        firstname VARCHAR(255) NOT NULL,
        lastname VARCHAR(255) NOT NULL,
        othernames VARCHAR(255),
        email VARCHAR(255) NOT NULL,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(500) NOT NULL,
        registered timestamp with time zone DEFAULT now(),
        isAdmin boolean DEFAULT FALSE,
        updatedOn timestamp with time zone
        );

        CREATE TABLE IF NOT EXISTS parcels(
            id SERIAL PRIMARY KEY,
            placedBy INTEGER NOT NULL,
            weight FLOAT,
            weightmetric VARCHAR(15),
            sentOn timestamp with time zone,
            deliveredOn timestamp with time zone,
            status VARCHAR(15) NOT NULL,
            "from" VARCHAR(255) NOT NULL,
            "to" VARCHAR(255) NOT NULL,
            currentlocation VARCHAR(255),
            isCanceled boolean DEFAULT FALSE,
            updatedOn timestamp with time zone,
            FOREIGN KEY (placedBy)
                REFERENCES users (id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
        self.cursor.execute(create_tables_command)
        return

#  CRUD Methods