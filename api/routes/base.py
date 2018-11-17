from flask import Blueprint


base_api = Blueprint('base_api', 'base_view', url_prefix='/api/v1')

@base_api.route('/')
def index():
    return 'SendIT Api'