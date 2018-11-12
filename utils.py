import re
import string
import random
import hashlib


def validate_email(str):
    return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", str)

def validate_alphanumeric(str):
    return re.match('^[a-zA-Z0-9]+$', str)

def string_generator(size):
    chars = string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size))

def encrypt_password(str):
    h = hashlib.md5(str.encode())
    return h.hexdigest()