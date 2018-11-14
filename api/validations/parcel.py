from utils import validate_float, validate_datetime, validate_integer
from api.database import DatabaseConnection


database = DatabaseConnection()

def validate_parcel_order(data):
    errors = {}
    # if not check_valid_parcel_data(data):
    #     errors['data'] = 'Unexpected order data'
    if not data.get('weight'):
        errors['no_weight'] = 'Weight can not be null'
    if not validate_float(data.get('weight')):
        errors['invalidweight'] = 'Invalid weight'
    if not data.get('weightmetric'):
        errors['weightmetric'] = 'Weight metric cannot be null'
    if not data.get('senton'):
        errors['validsenttime'] = 'Sent time can not be null'
    if not data.get('deliveredon'):
        errors['validdeliveredtime'] = 'Delivered time can not be null'
    if not data.get('from'):
        errors['from'] = 'Source can not be null'
    if not data.get('to'):
        errors['to'] = 'Destination field can not be null'
    if not data.get('currentlocation'):
        errors['currentlocation'] = 'Current location field can not be null'
    if not database.fetch_user_by_id(data.get('placedby')):
        errors['userid'] = 'user id does not exist'
    return errors

def validate_id(id):
    errors = {}
    if not id:
        errors['Id'] = 'Id field is required'
    if not validate_integer(id):
        errors['Id'] = 'Invalid interger format'
    return errors

def validate_userid(id):
    errors = {}
    if not database.fetch_user_by_id(id):
        errors['Id'] = 'User does not exist'
    return errors

def validate_parcel_order_id(id):
    errors = {}
    if not database.get_specific_parcel_order_id(id):
        errors['Id'] = 'Invalid parcel order'
    return errors

            