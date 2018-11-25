from api.routes import base
from flask import request, jsonify, Blueprint
from api.utils import encode_auth_token
import datetime
from api.validations.user import validate_user_registration_details, validate_null_user_data , validate_user_login_details, validate_if_isadmin, validate_userid
from api.models.user import User

  
user_api = Blueprint('user_api', 'user_api', url_prefix='/api/v1')

"""
POST  /auth/signup
{
    "username":"columbus",
    "email": "mugenyie@gmail.com",
    "firstname": "Emmanuel",
    "lastname": "mugenyie@gmail.com",
    "password": "12345"
}
CREATE A USER ACCOUNT 
"""
@user_api.route('/auth/signup', methods=['POST'])
def create_user():
    data = request.get_json(force=True)
    null_errors = validate_null_user_data(data)
    errors = validate_user_registration_details(data)
    errors.update(null_errors)
    if len(errors) > 0:
        return jsonify({
            'status': 400,
            'error' : errors
        }), 400
    data['registered'] = datetime.datetime.now()
    if not data.get('isAdmin'):
        data['isAdmin'] = False
    try:
        user = User(data).create_user()
        if user:
            return jsonify({
                'status': 201,
                'data': [{
                    'token': encode_auth_token(user.get('username')),
                    'user': user
                }]
            }), 201
    except Exception as e:
        print(e)
        return jsonify({
            'status': 400,
            'error' : str(e)
        }), 400

"""
POST  /auth/login 
LOGIN A USER
"""
@user_api.route('/auth/login', methods=['POST'])
def login_user():
    data = request.get_json(force=True)
    errors = validate_user_login_details(data)
    if len(errors) > 0:
        return jsonify({
            'status': 400,
            'error' : errors
        }), 400
    try:
        user = User(data).fetch_user_by_username_and_password()
        if user:
           return jsonify({
                'status': 200,
                'data': [{
                    'token': encode_auth_token(user.get('username')),
                    'user': user 
                }]
                }), 200  
        else:
            return jsonify({
                'status': 404,
                'error' : 'User does not exist'
            }), 404
    except Exception as e:
        print(e)
        return jsonify({
            'status': 400,
            'error' : str(e),
        }), 400

