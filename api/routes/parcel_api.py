from api.routes import base
from flask import request, jsonify, Blueprint
import datetime
from api.validations.parcel import validate_id, validate_parcel_order_id, check_is_delivered, validate_parcel_data
from api.validations.user import validate_userid, validate_if_isadmin
from api.order_status_enum import OrderStatus
from api.models.parcel import Parcel
from api.utils import token_required, encode_auth_token



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
@token_required
def create_parcel_delivery_order():
    data = request.get_json(force=True)
    if validate_userid(data.get('placedby')):
        return jsonify({
            'status': 404,
            'error' : 'User not found'
        }), 404
    errors = validate_parcel_data(data)
    if len(errors) > 0:
        return jsonify({
            'status': 400,
            'error' : errors
        }), 400
    data['senton'] = datetime.datetime.now()
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
            'status': 400,
            'error' : str(e),
        }), 400

"""
GET /parcels 
FETCH ALL PARCEL DELIVERY ORDERS 
"""
@parcel_api.route('/parcels', methods=['GET'])
@token_required
def get_all_parcels():
    try:
        parcels = Parcel().get_all_parcel_order()
        return jsonify({
            'status': 200,
            'data': parcels
        }), 200
    except Exception as e:
        return jsonify({
            'status': 400,
            'error' : str(e),
        }), 400

"""
GET /parcels/<parcelId> 
FETCH A SPECIFIC DELIVERY ORDER 
"""
@parcel_api.route('/parcels/<int:parcelId>', methods=['GET'])
@token_required
def get_specific_delivery_order(parcelId):
    try:
        parcel = Parcel({'parcelId':parcelId}).get_specific_parcel_order()
        if parcel:
            return jsonify({
                'status': 200,
                'data': parcel
            }), 200
        else:
            return jsonify({
                'status': 404,
                'error' : 'Order not found',
            }), 404
    except Exception as e:
        return jsonify({
            'status': 400,
            'error' : str(e),
        }), 400

"""
GET /users/<userId>/parcels 
FETCH ALL PARCEL DELIVERY ORDERS BY A SPECIFIC USER
"""
@parcel_api.route('/users/<int:userId>/parcels', methods=['GET'])
@token_required
def get_user_delivery_orders(userId):
    errors = validate_userid(userId)
    if len(errors) > 0:
        return jsonify({
            'status': 404,
            'error' : 'User not found'
        }), 404
    try:
        parcel = Parcel({'placedby': userId}).get_parcel_orders_by_user()
        if parcel:
            return jsonify({
                'status': 200,
                'data': parcel
            }), 200
        else:
            return jsonify({
                'status': '404',
                'error' : 'Order not found',
            }), 404
    except Exception as e:
        return jsonify({
            "Error" : str(e),
        }), 400

"""
PATCH  /parcels/<parcelId>/cancel 
CANCEL A SPECIFIC DELIVERY ORDER 
"""
@parcel_api.route('/parcels/<int:parcelId>/cancel', methods=['PATCH'])
@token_required
def cancel_delivery_order(parcelId):
    if validate_parcel_order_id(parcelId):
        return jsonify({
            'status': 404,
            'error' : 'Order not found'
        }), 404
    if check_is_delivered(parcelId):
        return jsonify({
            'status': 400,
            'error' : 'Order already delivered can not be canceled'
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
            'status': 400,
            'error' : str(e),
        }), 400


"""
PATCH  /parcels/<parcelId>/destination 
CHANGE DESTINATION OF SPECIFIC PARCEL DELIVERY ORDER
"""
@parcel_api.route('/parcels/<int:parcelId>/destination', methods=['PATCH'])
@token_required
def change_destination_parcel_delivery_order(parcelId):
    data = request.get_json(force=True)
    if validate_parcel_order_id(parcelId):
        return jsonify({
            'status': 404,
            'error' : 'Order not found'
        }), 404
    errors = {}
    if not data.get('to'):
        errors.update({'to':'Destination can not be null'})
    if check_is_delivered(parcelId):
        errors.update({'parcelId':'Order already delivered can not be canceled'})
    if errors:
        return jsonify({
            'status': 400,
            'error' : errors
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
            'status': 400,
            'error' : str(e),
        }), 400


"""
PATCH  /parcels/<parcelId>/status 
Change the status of a specific parcel delivery order
Only Admin
"""
@parcel_api.route('/parcels/<int:parcelId>/status', methods=['PATCH'])
@token_required
def change_status_parcel_delivery_order(parcelId):
    data = request.get_json(force=True)
    if validate_if_isadmin(data.get('userId')):
        return jsonify({
            'status': 401,
            'error' : 'Only admin authorised to access the resource'
        }), 401
    if not Parcel({"parcelId": parcelId}).get_specific_parcel_order():
        return jsonify({
            'status': 404,
            'error' : 'Parcel order not found'
        }), 404
    if not data.get('status'):
        return jsonify({
            'status': 400,
            'error' : 'Order status can not be null'
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
            'status': 400,
            'error' : str(e),
        }), 400


"""
PATCH  /parcels/<parcelId>/currentlocation 
Change the present location of a specific parcel delivery order.
Only Admin
"""
@parcel_api.route('/parcels/<int:parcelId>/currentlocation', methods=['PATCH'])
@token_required
def change_present_location_of_order(parcelId):
    data = request.get_json(force=True)
    if validate_if_isadmin(data.get('userId')):
        return jsonify({
            'status': 401,
            'error' : 'Only admin authorised to access the resource'
        }), 401
    if not Parcel({"parcelId": parcelId}).get_specific_parcel_order():
        return jsonify({
            'status': 404,
            'error' : 'Parcel order not found'
        }), 404
    if not data.get('currentlocation'):
        return jsonify({
            'status': 400,
            'error' : 'Current location can not be null'
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
            'status': 400,
            'error' : str(e),
        }), 400
