import re
import jwt
import string
import random
from functools import wraps
import hashlib
import datetime
from flask import request, jsonify, make_response, Flask
import smtplib


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ColumbusIsTheRealestProgramer'


def validate_email(str):
    return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", str)

def validate_alphanumeric(str):
    return re.match('^[a-zA-Z0-9]+$', str)

def validate_float(float_):
    return re.match('[+-]?([0-9]*[.])?[0-9]+',float_)

def validate_integer(interger):
    return re.match(r'^[0-9]*$',interger)

def validate_datetime(date_time):
    return datetime.datetime.strptime(date_time, '%m/%j/%y %H:%M')

def string_generator(size):
    chars = string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size)) 

def encrypt_password(str):
    h = hashlib.md5(str.encode())
    return h.hexdigest()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({
                'status': 401,
                'error': 'Token is missing, please login to get token'
                }), 401
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithm='HS256')
        except jwt.ExpiredSignatureError:
            return jsonify({
                'status': 401,
                'error': 'Token expired, please login'
                }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'status': 401,
                'error': 'Invalid token, please login'
                }), 401
        return f(*args, **kwargs)
    return decorated

def encode_auth_token(username):
    payload = {
        'user': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 30),
    }
    return jwt.encode(
        payload, 
        app.config['SECRET_KEY'],
        algorithm='HS256'
        ).decode('UTF-8')

def send_email(to, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("senditcolumbus@gmail.com", "Sendit123")
    fromaddr = "senditcolumbus@gmail.com"
    text = 'Subject: {}\n\n{}'.format(subject, message)
    server.sendmail(fromaddr, to, text)