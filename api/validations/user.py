import re
from utils import validate_alphanumeric, validate_email, encrypt_password
from api.database import DatabaseConnection


database = DatabaseConnection()

def validate_user_registration_details(data):
    errors = {}
    if not validate_email(data.get('email')):
        errors['email'] = 'Please enter a valid email'
    if not data.get('password'):
        errors['password'] = 'Password required'
    if not data.get('username'):
        errors['username'] = 'Username required'    
    if database.fetch_user_by_email(data.get('email')):
        errors['duplicate_email'] = 'Email already registered'
    if database.fetch_user_by_username(data.get('username')):
        errors['duplicate_username'] = 'Username already registered'    
    if not validate_alphanumeric(data.get('username')):
        errors['alphanumeric_username'] = 'Username should only contain alpanumeric characters'
    if not data.get('firstname'):
        errors['firstname'] = 'Firstname required'
    if not data.get('lastname'):
        errors['lastname'] = 'Lastname required'
    return errors

def validate_user_login_details(data):
    errors = {}
    if not data.get('username'):
        errors['username'] = 'Username required'
    if not validate_alphanumeric(data.get('username')):
        errors['alphanumeric_username'] = 'Username should only contain alpanumeric characters'
    if not data.get('password'):
        errors['password'] = 'Password required'
    if not errors:
        user = database.fetch_user_by_username_and_password(data)
        if not user:
            errors['user'] = 'User does not exist'
    return errors
    