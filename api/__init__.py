from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from api.routes.base import base_api
from api.routes.parcel_api import parcel_api
from api.routes.user_api import user_api


app = Flask(__name__)
CORS(app)


SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/api/v1'  
# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  
    API_URL,
    config={
        'app_name': "SendIT API Documentation"
    }
)

# Register blueprints
app.register_blueprint(base_api)
app.register_blueprint(parcel_api)
app.register_blueprint(user_api)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

