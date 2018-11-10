import psycopg2
from pprint import pprint
from datetime import datetime
import urllib.parse as urlparse

class DatabaseConnection:
    try:
        def __init__(self):
            self.connection = psycopg2.connect(
                dbname="sendit_db",
                user="postgres",
                password="columbus",
                host="localhost",
                port=5432
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            pprint("Connected!")

    except:
        pprint("Failed To Connect to Database")