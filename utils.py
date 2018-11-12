import re

def check_valid_charaters(strg, search=re.compile(r'[^a-z0-9.]').search):
    return not bool(search(strg))

def encode_auth_token(user_id, username=None):
    """
    Encodes a payload to generate JWT Token
    :param user_id: Logged in user Id
    :param username: string: Logged in username
    :return: JWT token
    :TODO add secret key to app configuration
    """
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=31, seconds=130),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id,
        'username': username
    }
    return jwt.encode(
        payload,
        'SECRET_KEY',
        algorithm='HS256'
    )


def decode_auth_token(auth_token):
    """ Validates the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        if is_blacklisted(auth_token):
            return 'Token has been blacklisted. Please log in again'
        payload = jwt.decode(auth_token, 'SECRET_KEY', algorithm='HS256')
        session['user_id'] = str(payload.get('sub'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Token Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'