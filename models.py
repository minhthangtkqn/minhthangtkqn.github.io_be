from app import db

class CarsModel(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    model = db.Column(db.String())
    doors = db.Column(db.Integer())

    def __init__(self, name, model, doors):
        self.name = name
        self.model = model
        self.doors = doors

    def __repr__(self):
        return f"<Car {self.name}>"

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'doors': self.doors
        }
# CARS MODEL


class FlashCardsModel(db.Model):
    __tablename__ = 'card'

    _id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())

    def __init__(self, _id, name, description):
        self._id = _id
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Flash card {self.name}>"

    def serialize(self):
        return {
            '_id': self._id,
            'name': self.name,
            'description': self.description,
        }