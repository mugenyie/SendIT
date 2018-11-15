from utils import validate_float, validate_datetime, validate_integer
from api.database import DatabaseConnection


database = DatabaseConnection()

def validate_parcel_order(data):
    errors = {}
    if not validate_float(data.get('weight')):
        errors['invalidweight'] = 'Invalid weight'
    if not data.get('placedby'):
        errors['user'] = 'User id can not be null'
    else:
        if not database.fetch_user_by_id(data.get('placedby')):
            errors['userid'] = 'User id does not exist'
    return errors

def validate_null_parcel_data(data):
    errors = {}
    if not data.get('weight'):
        errors['no_weight'] = 'Weight can not be null'
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

def validate_parcel_order_id(id):
    errors = {}
    if not database.get_specific_parcel_order_id(id):
        errors['Id'] = 'Invalid parcel order'
    return errors

def validate_parcel_destination(destination):
    errors = {}
    if not destination:
        errors['destination'] = 'Order destination can not be null'
    return errors
    
def validate_parcel_status(status):
    errors = {}
    if not status:
        errors['Status'] = 'Order status can not be null'
    return errors
    
def validate_parcel_location(currentlocation):
    errors = {}
    if not currentlocation:
        errors['currentlocation'] = 'Current location can not be null'
    return errors

            