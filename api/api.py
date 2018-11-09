from flask import Blueprint, request, jsonify, session
import psycopg2
import psycopg2.extras
from database import DatabaseConnection

api = Blueprint('api', 'api', url_prefix='/api/v1')


@api.route('/')
def index():
    # try:
    #     psycopg2.connect(
    #             dbname="sendit_db",
    #             user="postgres",
    #             password="columbus",
    #             host="localhost",
    #             port=5432
    #         )
    #     print("connected to database")
    # except:
    #     print("can't connect to database")
    return 'SendIT Api'