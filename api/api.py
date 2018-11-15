from flask import Blueprint, request, jsonify, session
import uuid
from api.database import DatabaseConnection
from api.validations.user import validate_user_registration_details, validate_user_login_details, validate_if_isadmin, validate_userid
from api.validations.parcel import validate_parcel_order, validate_id, validate_parcel_order_id, validate_parcel_destination, validate_parcel_status, validate_parcel_location
from utils import encrypt_password
import datetime



database = DatabaseConnection()
api = Blueprint('api', 'api', url_prefix='/api/v1')


@api.route('/')
def index():
    return 'SendIT Api'
  

"""
POST  /auth/signup
CREATE A USER ACCOUNT 
"""
@api.route('/auth/signup', methods=['POST'])
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
@api.route('/auth/login', methods=['POST'])
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


# Parcel delivery Endpoints
"""
POST /parcels: 
CREATE A PARCEL DELIVERY ORDER 
"""
@api.route('/parcels', methods=['POST'])
def create_parcel_delivery_order():
    data = request.get_json(force=True)
    errors = validate_parcel_order(data)
    if len(errors) > 0:
        return jsonify({
            "Errors" : errors
        }), 404
    try:
        parcel = database.creat_parcel_delivery_order(data)
        return jsonify({
            'status': 201,
            'data': [{
                'id': parcel[0],
                'message': 'Order created'
            }]
        }), 201
    except Exception as e:
        return jsonify({
            "Error" : str(e),
        }), 401

"""
GET /parcels 
FETCH ALL PARCEL DELIVERY ORDERS 
"""
@api.route('/parcels', methods=['GET'])
def get_all_parcels():
    try:
        parcels = database.get_all_parcel_order()
        return jsonify({
            'status': 200,
            'data': parcels
        }), 200
    except Exception as e:
        return jsonify({
            "Error" : str(e),
        }), 401

"""
GET /parcels/<parcelId> 
FETCH A SPECIFIC DELIVERY ORDER 
"""
@api.route('/parcels/<int:parcelId>', methods=['GET'])
def get_specific_delivery_order(parcelId):
    try:
        parcel = database.get_specific_parcel_order(parcelId)
        return jsonify({
            'status': 200,
            'data': parcel
        }), 200
    except Exception as e:
        return jsonify({
            "Error" : str(e),
        }), 401

"""
GET /users/<userId>/parcels 
FETCH ALL PARCEL DELIVERY ORDERS BY A SPECIFIC USER
"""
@api.route('/users/<int:userId>/parcels', methods=['GET'])
def get_user_delivery_orders(userId):
    errors = validate_userid(userId)
    if len(errors) > 0:
        return jsonify({
            "Errors" : errors
        }), 404
    try:
        parcel = database.get_parcel_orders_by_user(userId)
        return jsonify({
            'status': 200,
            'data': parcel
        }), 200
    except Exception as e:
        return jsonify({
            "Error" : str(e),
        }), 401

"""
PATCH  /parcels/<parcelId>/cancel 
CANCEL A SPECIFIC DELIVERY ORDER 
"""
@api.route('/parcels/<int:parcelId>/cancel', methods=['PATCH'])
def cancel_delivery_order(parcelId):
    errors = validate_parcel_order_id(parcelId)
    if len(errors) > 0:
        return jsonify({
            "Errors" : errors
        }), 404
    try:
        database.cancel_delivery_order(parcelId)
        return jsonify({
            'status': 200,
            'data': [{
                'id': parcelId,
                'message': 'Order canceled'
            }]
        }), 200
    except Exception as e:
        return jsonify({
            "Error" : str(e),
        }), 401


"""
PATCH  /parcels/<parcelId>/destination 
CHANGE DESTINATION OF SPECIFIC PARCEL DELIVERY ORDER
"""
@api.route('/parcels/<int:parcelId>/destination', methods=['PATCH'])
def change_destination_parcel_delivery_order(parcelId):
    data = request.get_json(force=True)
    errors_parcel = validate_parcel_order_id(parcelId)
    errors = validate_parcel_destination(data.get('to'))
    errors.update(errors_parcel)
    if len(errors) > 0:
        return jsonify({
            "Errors" : errors
        }), 400
    try:
        database.change_order_destination(parcelId, data.get('to'))
        return jsonify({
            'status': 200,
            'data': [{
                'id': parcelId, #the parcel
                'to': data.get('to'),
                'message': 'Parcel destination updated'
            }]
        }), 200
    except Exception as e:
        return jsonify({
            "Error" : str(e),
        }), 401


"""
PATCH  /parcels/<parcelId>/status 
Change the status of a specific parcel delivery order
Only Admin
"""
@api.route('/parcels/<int:parcelId>/status', methods=['PATCH'])
def change_status_parcel_delivery_order(parcelId):
    data = request.get_json(force=True)
    errors_parcel = validate_parcel_order_id(parcelId)
    errors_user = validate_if_isadmin(data.get('userid'))
    errors = validate_parcel_status(data.get('status'))
    errors.update(errors_parcel)
    errors.update(errors_user)
    if len(errors) > 0:
        if errors_user:
            return jsonify({
            "Errors" : errors_user
            }), 401
        else:
            return jsonify({
            "Errors" : errors
            }), 400
    try:
        database.change_order_status(parcelId, data.get('status'))
        return jsonify({
            'status': 200,
            'data': [{
                'id': parcelId, #the parcel
                'status': data.get('status'),
                'message': 'Parcel status updated'
            }]
        }), 200
    except Exception as e:
        return jsonify({
            "Error" : str(e),
        }), 401


"""
PATCH  /parcels/<parcelId>/currentlocation 
Change the present location of a specific parcel delivery order.
Only Admin
"""
@api.route('/parcels/<int:parcelId>/currentlocation', methods=['PATCH'])
def change_present_location_of_order(parcelId):
    data = request.get_json(force=True)
    errors = validate_parcel_order_id(parcelId)
    errors_user = validate_if_isadmin(data.get('userid'))
    errors_location = validate_parcel_location(data.get('currentlocation'))
    errors.update(errors_user)
    errors.update(errors_location)
    if len(errors) > 0:
        if errors_user:
            return jsonify({
            "Errors" : errors_user
            }), 401
        else:
            return jsonify({
            "Errors" : errors
            }), 400
    try:
        database.change_order_status(parcelId, data.get('currentlocation'))
        return jsonify({
            'status': 200,
            'data': [{
                'id': parcelId, #the parcel
                'currentLocation': data.get('currentlocation'),
                'message': 'Parcel location updated'
            }]
        }), 200
    except Exception as e:
        return jsonify({
            "Error" : str(e),
        }), 401