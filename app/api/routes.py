import logging
from flask import Blueprint, jsonify, request
from models import Car, CarSchema, db
from helpers import token_required

# Set up basic configuration for logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return jsonify({'yee': 'naw'})


@api.route('/cars', methods=['POST'])
@token_required
def create_car(current_user_token):
    data = request.json
    make = data.get('make')
    model = data.get('model')
    year = data.get('year')

    if not make or not model or not year:
        return jsonify({'error': 'Make, model, and year are required'}), 400

    car = Car(make=make, model=model, year=year, user_id=current_user_token.id)  # Ensure user_id is passed correctly
    db.session.add(car)
    db.session.commit()

    car_schema = CarSchema()  # Create an instance of CarSchema
    response = car_schema.dump(car)  # Dump the car object using the instance
    return jsonify(response), 201



@api.route('/cars', methods=['GET'])
@token_required
def get_cars(current_user_token):
    cars = Car.query.all()
    cars_schema = CarSchema(many=True)  # Ensure this is defined and imported correctly
    response = cars_schema.dump(cars)  # Serialize the list of cars
    return jsonify(response)

@api.route('/cars/<int:id>', methods=['GET'])
@token_required
def get_car(current_user_token, id):
    car = Car.query.get_or_404(id)
    return jsonify(car.to_dict())

@api.route('/cars/<int:id>', methods=['PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get_or_404(id)
    data = request.json

    car.make = data.get('make', car.make)
    car.model = data.get('model', car.model)
    car.year = data.get('year', car.year)
    car.color = data.get('color', car.color)  # Assuming color is a field you want to update
    car.price = data.get('price', car.price)  # Assuming price is also a field you want to update

    db.session.commit()

    car_schema = CarSchema()
    response = car_schema.dump(car)
    return jsonify(response), 200

@api.route('/cars/<string:id>', methods=['DELETE'])
@token_required
def delete_car(current_user_token, id):
    # Log the attempt to delete a car
    logging.debug(f"Attempting to delete car with ID: {id}")

    try:
        car = Car.query.get_or_404(id)
        car_schema = CarSchema()  # This is defined to serialize the car data
        response = car_schema.dump(car)  # Serialize the car data before deleting it

        # Log the car data that is about to be deleted
        logging.debug(f"Car data to be deleted: {response}")

        db.session.delete(car)
        db.session.commit()

        # Log successful deletion
        logging.debug(f"Car with ID: {id} deleted successfully")
        return jsonify(response), 200

    except Exception as e:
        # Log any errors encountered during the process
        logging.error(f"Error deleting car with ID: {id}, Error: {e}")
        return jsonify({'error': 'Failed to delete car', 'message': str(e)}), 500



# Helper function to convert car data to dictionary (if not already defined in the Car model)
def car_to_dict(car):
    return {
        'id': car.id,
        'make': car.make,
        'model': car.model,
        'year': car.year
    }
