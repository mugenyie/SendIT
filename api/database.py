import psycopg2
from pprint import pprint
from datetime import datetime
import urllib.parse as urlparse
from dotenv import load_dotenv
from urllib.parse import urlparse
import os


class DatabaseConnection:
    try:
        def __init__(self):
            load_dotenv()
            if os.environ.get('DATABASE_URL'):
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


    def create_user(self, data={}):
        insert_user_command = """
        INSERT INTO users (firstname, lastname, othernames, email, username, registered, password) 
        VALUES (%s,%s,%s,%s,%s,%s,%s) 
        RETURNING id,firstname, lastname, othernames, email, username, registered, isadmin
        """

        self.cursor.execute(insert_user_command, (
            data.get('firstname'), data.get('lastname'), 
            data.get('othernames'), data.get('email'), 
            data.get('username'), data.get('registered'), data.get('password')
        ))
        user = self.cursor.fetchone()
        return user

    def fetch_user_by_username(self, username):
        get_user_command = """
        SELECT * FROM users WHERE "username"= '{}';
        """.format(username)
        self.cursor.execute(get_user_command)

        user = self.cursor.fetchone()
        return user

    def fetch_user_by_email(self, email_address):
        get_user_by_email_command = """
        SELECT * FROM users WHERE "email"='{}'
        """.format(email_address)
        self.cursor.execute(get_user_by_email_command)

        user = self.cursor.fetchone()
        return user