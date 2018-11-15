from flask import Blueprint
import uuid
from api.database import DatabaseConnection
from utils import encrypt_password


database = DatabaseConnection()
base_api = Blueprint('base_api', 'base_view', url_prefix='/api/v1')

@base_api.route('/')
def index():
    return 'SendIT Api'