from api.routes import base
from flask import request, jsonify, Blueprint
import datetime
from api.validations.parcel import validate_id, validate_parcel_order_id, validate_parcel_destination, validate_change_order_status, validate_parcel_location, check_is_delivered, validate_parcel_data
from api.validations.user import validate_userid, validate_if_isadmin
from api.order_status_enum import OrderStatus
from api.models.parcel import Parcel



parcel_api = Blueprint('parcel_api', 'parcel_api', url_prefix='/api/v1')

"""
POST /parcels: 
{
	"placedby": 87,
    "to": "87",
    "from": "kamwokya",
    "weight": 4,
    "weightmetric": "Kg"
}
CREATE A PARCEL DELIVERY ORDER 
"""
@parcel_api.route('/parcels', methods=['POST'])
def create_parcel_delivery_order():
    data = request.get_json(force=True)
    if validate_userid(data.get('placedby')):
        return jsonify({
            "Errors" : "User not found"
        }), 404
    errors = validate_parcel_data(data)
    if len(errors) > 0:
        return jsonify({
            "Errors" : errors
        }), 400
    try:
        parcel = Parcel(data).creat_parcel_delivery_order()
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
        }), 400

"""
GET /parcels 
FETCH ALL PARCEL DELIVERY ORDERS 
"""
@parcel_api.route('/parcels', methods=['GET'])
def get_all_parcels():
    try:
        parcels = Parcel().get_all_parcel_order()
        return jsonify({
            'status': 200,
            'data': parcels
        }), 200
    except Exception as e:
        return jsonify({
            "Error" : str(e),
        }), 400

"""
GET /parcels/<parcelId> 
FETCH A SPECIFIC DELIVERY ORDER 
"""
@parcel_api.route('/parcels/<int:parcelId>', methods=['GET'])
def get_specific_delivery_order(parcelId):
    try:
        parcel = Parcel({'parcelId':parcelId}).get_specific_parcel_order()
        return jsonify({
            'status': 200,
            'data': parcel
        }), 200
    except Exception as e:
        return jsonify({
            "Error" : str(e),
        }), 400

"""
GET /users/<userId>/parcels 
FETCH ALL PARCEL DELIVERY ORDERS BY A SPECIFIC USER
"""
@parcel_api.route('/users/<int:userId>/parcels', methods=['GET'])
def get_user_delivery_orders(userId):
    errors = validate_userid(userId)
    if len(errors) > 0:
        return jsonify({
            "Errors" : "User not found"
        }), 404
    try:
        parcel = Parcel({'placedby': userId}).get_parcel_orders_by_user()
        return jsonify({
            'status': 200,
            'data': parcel
        }), 200
    except Exception as e:
        return jsonify({
            "Error" : str(e),
        }), 400

"""
PATCH  /parcels/<parcelId>/cancel 
CANCEL A SPECIFIC DELIVERY ORDER 
"""
@parcel_api.route('/parcels/<int:parcelId>/cancel', methods=['PATCH'])
def cancel_delivery_order(parcelId):
    if validate_parcel_order_id(parcelId):
        return jsonify({
            "Errors" : "Parcel order not found"
        }), 404
    if check_is_delivered(parcelId):
        return jsonify({
            "Errors" : "Delivered order can not be canceled"
        }), 400
    try:
        Parcel({'parcelId': parcelId}).cancel_delivery_order()
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
        }), 400


"""
PATCH  /parcels/<parcelId>/destination 
CHANGE DESTINATION OF SPECIFIC PARCEL DELIVERY ORDER
"""
@parcel_api.route('/parcels/<int:parcelId>/destination', methods=['PATCH'])
def change_destination_parcel_delivery_order(parcelId):
    data = request.get_json(force=True)
    if validate_parcel_order_id(parcelId):
        return jsonify({
            "Errors" : "Parcel order not found"
        }), 404
    if check_is_delivered(parcelId):
        return jsonify({
            "Errors" : "Delivered order can not be canceled"
        }), 400
    errors = validate_parcel_destination(data.get('to'))
    if len(errors) > 0:
        return jsonify({
            "Errors" : errors
        }), 400
    try:
        Parcel({'parcelId': parcelId, 'to': data.get('to')}).change_order_destination()
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
        }), 400


"""
PATCH  /parcels/<parcelId>/status 
Change the status of a specific parcel delivery order
Only Admin
"""
@parcel_api.route('/parcels/<int:parcelId>/status', methods=['PATCH'])
def change_status_parcel_delivery_order(parcelId):
    data = request.get_json(force=True)
    if validate_if_isadmin(data.get('userId')):
        return jsonify({
            "Errors" : "Only admin authorised to access the resource"
        }), 401
    if not Parcel({"parcelId": parcelId}).get_specific_parcel_order():
        return jsonify({
            "Errors" : "Parcel order not found"
        }), 401
    if not data.get('status'):
        return jsonify({
            "Errors" : "Order status can not be null"
        }), 400
    try:
        Parcel({'parcelId': parcelId, 'status': data.get('status')}).change_order_status()
        return jsonify({
            'status': 200,
            'data': [{
                'id': parcelId, #the parcel
                'status': data.get('status').upper(),
                'message': 'Parcel status updated'
            }]
        }), 200
    except Exception as e:
        return jsonify({
            "Error" : str(e),
        }), 400


"""
PATCH  /parcels/<parcelId>/currentlocation 
Change the present location of a specific parcel delivery order.
Only Admin
"""
@parcel_api.route('/parcels/<int:parcelId>/currentlocation', methods=['PATCH'])
def change_present_location_of_order(parcelId):
    data = request.get_json(force=True)
    if validate_if_isadmin(data.get('userId')):
        return jsonify({
            "Errors" : "Only admin authorised to access the resource"
        }), 401
    if not Parcel({"parcelId": parcelId}).get_specific_parcel_order():
        return jsonify({
            "Errors" : "Parcel order not found"
        }), 401
    if not data.get('currentlocation'):
        return jsonify({
            "Errors" : "Current location can not be null"
        }), 400
    try:
        Parcel({'parcelId': parcelId, 'currentlocation': data.get('currentlocation')}).change_order_status()
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
        }), 400