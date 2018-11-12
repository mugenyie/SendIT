import re
from api.database import DatabaseConnection


database = DatabaseConnection()

def validate_user_registration_details(data):
    errors = {}
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", data.get('email').strip()):
        errors['email'] = 'Invalid email. Please enter a valid email'
    if not data.get('password'):
        errors['password'] = 'Password required'
    if not data.get('username').strip():
        errors['username'] = 'Username required'    
    if database.fetch_user_by_email(data.get('email').strip()):
        errors['duplicate_email'] = 'Email already registered'
    if database.fetch_user_by_username(data.get('username').strip()):
        errors['duplicate_username'] = 'Username already registered'    
    if not re.match('^[a-zA-Z0-9]+$', data.get('username').strip()):
        errors['alphanumeric_username'] = 'Username should only contain alpanumeric characters'
    if not data.get('firstname').strip():
        errors['firstname'] = 'Firstname required'
    if not data.get('lastname').strip():
        errors['lastname'] = 'Lastname required'
    return errors