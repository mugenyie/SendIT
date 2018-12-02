from flask import Blueprint, send_from_directory


base_api = Blueprint('base_api', 'base_view', url_prefix='/api/v1')
swagger_json = Blueprint('swagger_json','base_view',static_folder='static',static_url_path='/static')

@base_api.route('/')
def index():
    return """
    SendIT API
    [API Documentation: https://sendit-api-columbus.herokuapp.com/api/v1/docs/]
    """

@swagger_json.route('/v1/swagger.json')
def swagger():
    return send_from_directory('static','swagger.json')