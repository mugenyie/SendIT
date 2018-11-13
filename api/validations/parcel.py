from utils import validate_float, validate_datetime
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

            