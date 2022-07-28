from app import app, db
from flask import Flask, request, jsonify

from models import CarsModel, FlashCardsModel

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/name/<name>")
def get_book_name(name):
    return "name : {}".format(name)


@app.route("/details")
def get_book_details():
    author = request.args.get('author')
    published = request.args.get('published')
    return "Author : {}, Published: {}".format(author, published)


@app.route('/cars', methods=['POST', 'GET'])
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


@app.route('/cars/<car_id>', methods=['GET', 'PUT', 'DELETE'])
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


@app.route('/flash_cards', methods=['POST', 'GET'])
def handle_cards():
    print('HANDLE FLASH CARDS POSTING')
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_card = FlashCardsModel(
                _id=data['_id'],
                name=data['name'],
                description=data['description']
            )
            db.session.add(new_card)
            db.session.commit()
            return {"message": f"card {new_card.name} has been created successfully."}
        else:
            return {'error': 'The request payload is not in JSON format'}
    elif request.method == 'GET':
        cars = FlashCardsModel.query.all()
        result = [{
            "_id": car._id,
            "name": car.name,
            "description": car.description,
        } for car in cars]

        if(type(result) is list):
            print('BINGO')

        return jsonify(result)


@app.route('/flash_card/<card_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_flash_card(card_id):
    card = FlashCardsModel.query.get_or_404(card_id)

    if request.method == 'GET':
        response = {
            "_id": card._id,
            "name": card.name,
            "description": card.description,
        }
        return {"message": "success", "flash card": response}

    elif request.method == 'PUT':
        data = request.get_json()
        card.name = data['name']
        card.description = data['description']
        db.session.add(card)
        db.session.commit()
        return {"message": f"Card {card.name} successfully updated."}

    elif request.method == 'DELETE':
        db.session.delete(card)
        db.session.commit()
        return {"message": f"Card {card.name} successfully deleted."}


if __name__ == '__main__':
    app.run()