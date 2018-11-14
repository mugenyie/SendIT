import re
import string
import random
import hashlib
import datetime


def validate_email(str):
    return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", str)

def validate_alphanumeric(str):
    return re.match('^[a-zA-Z0-9]+$', str)

def validate_float(float_):
    return re.match(r'[-+]?([0-9]*\.[0-9]+|[0-9]+)',float_)

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

# def is_valid_parcel_data(data={}):
#     order = dict(
#             placedby="w",
#             weight="w",
#             weightmetric="w",
#             senton= "w",
#             deliveredon= "w",
#             to="w",
#             currentlocation="w"
#         )
#     order['from'] ="w"

#     return any(True  for k in order if k not in data)
