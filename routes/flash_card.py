from app import db
from models import FlashCardsModel
from flask import request, jsonify, Blueprint


flash_card_api = Blueprint('flash_card_api', __name__, template_folder='templates')


@flash_card_api.route('/flash_cards', methods=['POST', 'GET'])  # FLASHCARD ROUTING
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


@flash_card_api.route('/flash_card/<card_id>', methods=['GET', 'PUT', 'DELETE'])
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
