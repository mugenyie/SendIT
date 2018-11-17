import re
from utils import validate_alphanumeric, validate_email, encrypt_password
from api.models.parcel import Parcel
from api.models.user import User



def validate_null_user_data(data):
    errors = {}
    if not data.get('password'):
        errors['password'] = 'Password required'
    if not data.get('username'):
        errors['username'] = 'Username required' 
    if not data.get('firstname'):
        errors['firstname'] = 'Firstname required'
    if not data.get('lastname'):
        errors['lastname'] = 'Lastname required'
    if not data.get('email'):
        errors['email'] = 'Email is required'
    return errors 

def validate_user_registration_details(data):
    errors = {}
    if not validate_email(data.get('email')):
        errors['email'] = 'Please enter a valid email'  
    if User(data).fetch_user_by_email():
        errors['duplicate_email'] = 'Email already registered'
    if User(data).fetch_user_by_username():
        errors['duplicate_username'] = 'Username already registered'    
    if not validate_alphanumeric(data.get('username')):
        errors['alphanumeric_username'] = 'Username can only contain alpanumeric characters'
    return errors

def validate_user_login_details(data):
    errors = {}
    if not data.get('username').strip():
        errors['username'] = 'Username required'
    if not data.get('password'):
        errors['password'] = 'Password required'
    if not validate_alphanumeric(data.get('username')):
        errors['alphanumeric_username'] = 'Username can only contain alpanumeric characters'
    return errors

def validate_if_isadmin(userId):
    errors = {}
    if not userId:
        errors['user'] = 'User id can not be null'
    else:
        if not User({"userId": userId}).check_if_isadmin():
            errors['user'] = 'Only admin is allowed to access the resource'
    return errors

def validate_userid(userId):
    errors = {}
    if not userId:
        errors['id'] = 'User id can not be null'
    if not User({"userId": userId}).fetch_user_by_id():
        errors['id'] = 'User does not exist'
    return errors

    