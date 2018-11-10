from flask import Blueprint, request, jsonify, session
import psycopg2
import psycopg2.extras
from database import DatabaseConnection

api = Blueprint('api', 'api', url_prefix='/api/v1')


@api.route('/')
def index():
    return 'SendIT Api'


@api.route('/parcels')
def get_parcels():
    return 'parcel'


@api.route('/parcels/<parcelId>')
def get_specific_delivery_order():
    return 'order'