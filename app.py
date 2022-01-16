from crypt import methods
from urllib import response
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_object("config.DevelopmentConfig")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ======================================================

# CARS MODEL


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

if __name__ == '__main__':
    app.run()
