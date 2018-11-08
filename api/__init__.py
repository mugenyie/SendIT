from flask import Flask
# Blueprints
from api.api import api

app = Flask(__name__)

app.register_blueprint(api)