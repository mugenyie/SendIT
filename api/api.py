from flask import Blueprint, request, jsonify, session

api = Blueprint('api', 'api', url_prefix='/api/v1')


@api.route('/')
def index():
    return 'SendIT Api'