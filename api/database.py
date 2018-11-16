import psycopg2
from pprint import pprint
from datetime import datetime
import urllib.parse as urlparse
from dotenv import load_dotenv
from urllib.parse import urlparse
from utils import encrypt_password
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


#  CRUD Methods
    def create_user(self, data={}):
        insert_user_command = """
        INSERT INTO users (firstname, lastname, othernames, email, username, registered, password) 
        VALUES (%s,%s,%s,%s,%s,%s,%s) 
        RETURNING id,firstname, lastname, othernames, email, username, registered, isadmin
        """
        self.cursor.execute(insert_user_command, (
            data.get('firstname'), data.get('lastname'), 
            data.get('othernames'), data.get('email'), 
            data.get('username'), data.get('registered'), encrypt_password(data.get('password'))
        ))
        user = self.cursor.fetchone()
        person = {}
        person['id'] = user[0]
        person['firstname'] = user[1]
        person['lastname'] = user[2]
        person['othernames'] = user[3]
        person['email'] = user[4]
        person['username'] = user[5]
        person['registered'] = user[6]
        person['isAdmin'] = user[7]
        return person

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

    def fetch_user_by_id(self, id_):
        get_user_by_id_command = """
        SELECT * FROM users WHERE "id"='{}'
        """.format(id_)
        self.cursor.execute(get_user_by_id_command)
        user = self.cursor.fetchone()
        return user
    
    def check_if_isadmin(self, id_):
        get_user_by_id_command = """
        SELECT * FROM users WHERE id = {} and isadmin = True
        """.format(id_)
        self.cursor.execute(get_user_by_id_command)
        user = self.cursor.fetchone()
        return user

    def fetch_user_by_username_and_password(self, data={}):
        get_user_command = """
        SELECT id,firstname, lastname, othernames, email, username, registered, isadmin
        FROM users WHERE "username" ='{}' AND "password" ='{}'
        """.format(data.get('username'), encrypt_password(data.get('password')))
        user = self.cursor.execute(get_user_command)
        user = self.cursor.fetchone()
        person = {}
        if user:
            person['id'] = user[0]
            person['firstname'] = user[1]
            person['lastname'] = user[2]
            person['othernames'] = user[3]
            person['email'] = user[4]
            person['username'] = user[5]
            person['registered'] = user[6]
            person['isAdmin'] = user[7]
        return person

#Parcel CRUD operations
    def creat_parcel_delivery_order(self, data={}):
        get_parcel_command = """
        INSERT INTO parcels (placedby, weight, weightmetric, senton, status, "from", "to")
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        RETURNING id, placedby, weight, weightmetric, senton, status, "from", "to"
        """
        self.cursor.execute(get_parcel_command, (
            data.get('placedby'), data.get('weight'), 
            data.get('weightmetric'), data.get('senton'), 
            "PLACED", 
            data.get('from'), data.get('to')
        ))
        parcel = self.cursor.fetchone()
        return parcel

    def get_all_parcel_order(self):
        get_parcel_orders_command = """
        SELECT id, placedby, weight, weightmetric, senton, deliveredon,status, "from", "to", currentlocation
        from parcels 
        """
        self.cursor.execute(get_parcel_orders_command)
        columns = [col[0] for col in self.cursor.description]
        parcels = [dict(zip(columns, parcel)) for parcel in self.cursor.fetchall()]        
        return parcels

    def get_specific_parcel_order(self, parcelId):
        get_parcel_orders_command = """
        SELECT id, placedby, weight, weightmetric, senton, deliveredon,status, "from", "to", currentlocation
        from parcels WHERE id = {}
        """.format(parcelId)
        self.cursor.execute(get_parcel_orders_command)
        columns = [col[0] for col in self.cursor.description]
        parcels = [dict(zip(columns, parcel)) for parcel in self.cursor.fetchall()]        
        return parcels

    def get_specific_parcel_order_id(self, parcelId):
        get_parcel_orders_command = """
        SELECT * from parcels WHERE id = {}
        """.format(parcelId)
        self.cursor.execute(get_parcel_orders_command)
        parcel = self.cursor.fetchone()
        return parcel

    def get_parcel_orders_by_user(self, userId):
        get_parcel_orders_command = """
        SELECT id, placedby, weight, weightmetric, senton, deliveredon,status, "from", "to", currentlocation
        from parcels WHERE placedby = {}
        """.format(userId)
        self.cursor.execute(get_parcel_orders_command)
        columns = [col[0] for col in self.cursor.description]
        parcels = [dict(zip(columns, parcel)) for parcel in self.cursor.fetchall()]        
        return parcels

    def cancel_delivery_order(self, parcelId):
        cancel_parcel_order = """
        UPDATE parcels SET iscanceled = True WHERE id = {}
        """.format(parcelId)
        self.cursor.execute(cancel_parcel_order)   
        return 

    def change_order_destination(self, parcelId, destination):
        change_destination_commnd = """
        UPDATE parcels SET "to" = '{}' WHERE id = {}
        """.format(destination, parcelId)
        self.cursor.execute(change_destination_commnd)   
        return 

    def change_order_status(self, parcelId, status):
        change_status_commnd = """
        UPDATE parcels SET "status" = '{}' WHERE id = {}
        """.format(status, parcelId)
        self.cursor.execute(change_status_commnd)   
        return 