from api.views import base_view
from flask import request, jsonify, Blueprint
import datetime
from api.validations.user import validate_user_registration_details, validate_user_login_details, validate_if_isadmin, validate_userid
  
  
database = base_view.database
user_api = Blueprint('user_api', 'user_view_api', url_prefix='/api/v1')

"""
POST  /auth/signup
CREATE A USER ACCOUNT 
"""
@user_api.route('/auth/signup', methods=['POST'])
def create_user():
    data = request.get_json(force=True)
    errors = validate_user_registration_details(data)
    if len(errors) > 0:
        return jsonify({
            "Errors" : errors
        }), 404
    data['registered'] = datetime.datetime.now()
    try:
        user = database.create_user(data)
        return jsonify({
            'status': 201,
            'data': [{
                'token': '',
                'user': user
            }]
        }), 201
    except Exception as e:
        print(e)
        return jsonify({
            "Error" : str(e)
        }), 401

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
            "Errors" : errors
        }), 404
    try:
        user = database.fetch_user_by_username_and_password(data)
        return jsonify({
            'status': 200,
            'data': [{
                'token': '',
                'user': user 
            }]
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            "Error" : str(e),
        }), 401

