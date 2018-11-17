from utils import validate_float, validate_datetime, validate_integer
from api.order_status_enum import OrderStatus
from api.models.parcel import Parcel
from api.models.user import User
from flask import jsonify


def validate_parcel_data(data):
    errors = {}
    if not data.get('weight'):
        errors['no_weight'] = 'Weight can not be null'
    else:
        if not validate_float(data.get('weight')):
            errors['invalidweight'] = 'Invalid weight'
    if not data.get('to'):
        errors['to'] = 'Destination field can not be null'
    if not data.get('from'):
        errors['from'] = 'Source can not be null'
    if not data.get('weightmetric'):
        errors['weightmetric'] = 'Weight metric cannot be null'
    return errors

def validate_id(id):
    errors = {}
    if not id:
        errors['Id'] = 'Id field is required'
    if not validate_integer(id):
        errors['Id'] = 'Invalid interger format'
    return errors

def validate_parcel_order_id(parcelId):
    errors = {}
    if not Parcel({'parcelId': parcelId}).get_specific_parcel_order():
        errors['parcelId'] = 'Parcel order not found'
    return errors

def validate_parcel_destination(destination):
    errors = {}
    if not destination:
        errors['destination'] = 'Order destination can not be null'
    return errors
    
def validate_change_order_status(data):
    errors = {}
    if not data.get('status'):
        errors['Status'] = 'Order status can not be null'
    return errors
    
def validate_parcel_location(currentlocation):
    errors = {}
    if not currentlocation:
        errors['currentlocation'] = 'Current location can not be null'
    return errors

def check_is_delivered(parcelId):
    errors = {}
    order_status = Parcel({"parcelId": parcelId}).check_order_status()
    if order_status.upper() == 'DELIVERED':
        errors['status'] = 'Delivered order can not be canceled'
    return errors