from app import db
from models import CarsModel
from flask import request, Blueprint

car_api = Blueprint('car_api', __name__, template_folder='templates')


@car_api.route('/cars', methods=['POST', 'GET'])    # CAR ROUTING
def handle_cars():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_car = CarsModel(
                name=data['name'], model=data['model'], doors=data['doors'])
            db.session.add(new_car)
            db.session.commit()
            return {"message": f"car {new_car.name} has been created successfully."}
        else:
            return {'error': 'The request payload is not in JSON format'}
    elif request.method == 'GET':
        cars = CarsModel.query.all()
        result = [{
            "id": car.id,
            "name": car.name,
            "model": car.model,
            "doors": car.doors
        } for car in cars]

        return {'count': len(result), 'cars': result}


@car_api.route('/cars/<car_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_car(car_id):
    car = CarsModel.query.get_or_404(car_id)

    if request.method == 'GET':
        response = {
            "id": car.id,
            "name": car.name,
            "model": car.model,
            "doors": car.doors
        }
        return {"message": "success", "car": response}

    elif request.method == 'PUT':
        data = request.get_json()
        car.name = data['name']
        car.model = data['model']
        car.doors = data['doors']
        db.session.add(car)
        db.session.commit()
        return {"message": f"car {car.name} successfully updated."}

    elif request.method == 'DELETE':
        db.session.delete(car)
        db.session.commit()
        return {"message": f"car {car.name} successfully deleted."}
