from flask import jsonify, request, Blueprint
from models import db, Car, car_schema, cars_schema  # Updated imports

api = Blueprint('api', __name__)