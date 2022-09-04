from app import app
from flask import request
from routes.flash_card import flash_card_api
from routes.car import car_api

app.register_blueprint(flash_card_api)
app.register_blueprint(car_api)

@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run()


@app.route("/name/<name>")
def get_book_name(name):
    return "name : {}".format(name)


@app.route("/details")
def get_book_details():
    author = request.args.get('author')
    published = request.args.get('published')
    return "Author : {}, Published: {}".format(author, published)

