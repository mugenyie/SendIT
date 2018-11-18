from api.models.database import DatabaseConnection
from utils import encrypt_password


database = DatabaseConnection()
class User: 
    def __init__(self, data={}):
        self.userId = data.get('userId')
        self.firstname = data.get('firstname')
        self.lastname = data.get('lastname')
        self.othernames = data.get('othernames')
        self.email = data.get('email')
        self.username = data.get('username')
        self.registered = data.get('registered')
        self.isAdmin = data.get('isAdmin')
        if data.get('password'):
            self.password = encrypt_password(data.get('password'))

    def create_user(self):
        insert_user_command = """
        INSERT INTO users (firstname, lastname, othernames, email, username, registered, password) 
        VALUES (%s,%s,%s,%s,%s,%s,%s) 
        RETURNING id,firstname, lastname, othernames, email, username, registered, isadmin
        """
        database.cursor.execute(insert_user_command, (
            self.firstname, self.lastname, 
            self.othernames, self.email, 
            self.username, self.registered, self.password
        ))
        user = database.cursor.fetchone()
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

    def fetch_user_by_username(self):
        get_user_command = """
        SELECT * FROM users WHERE "username"= '{}';
        """.format(self.username)
        database.cursor.execute(get_user_command)
        user = database.cursor.fetchone()
        return user

    def fetch_user_by_email(self):
        get_user_by_email_command = """
        SELECT * FROM users WHERE "email"='{}'
        """.format(self.email)
        database.cursor.execute(get_user_by_email_command)
        user = database.cursor.fetchone()
        return user

    def fetch_user_by_id(self):
        get_user_by_id_command = """
        SELECT * FROM users WHERE "id"={}
        """.format(self.userId)
        database.cursor.execute(get_user_by_id_command)
        user = database.cursor.fetchone()
        return user
    
    def check_if_isadmin(self):
        get_user_by_id_command = """
        SELECT * FROM users WHERE id = {} and isadmin = True
        """.format(self.userId)
        database.cursor.execute(get_user_by_id_command)
        user = database.cursor.fetchone()
        return user

    def fetch_user_by_username_and_password(self):
        get_user_command = """
        SELECT id,firstname, lastname, othernames, email, username, registered, isadmin
        FROM users WHERE "username" ='{}' AND "password" ='{}'
        """.format(self.username, self.password)
        user = database.cursor.execute(get_user_command)
        user = database.cursor.fetchone()
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