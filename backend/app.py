import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_sqlalchemy import SQLAlchemy

from backend.security import authenticate, identity
from backend.resources.items import ItemResource, ItemList
from backend.resources.users import UserRegister
from secrets import SECRET_KEY


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.dirname(os.path.realpath(__file__))}//data.db'
    db = SQLAlchemy(app)
    with app.app_context():
        db.create_all()
    db.session.commit()
    api = Api(app)

    app.config['SECRET_KEY'] = SECRET_KEY
    jwt = JWT(app, authenticate, identity)

    api.add_resource(ItemResource, '/items/<string:name>')
    api.add_resource(ItemList, '/items')
    api.add_resource(UserRegister, '/register')

    return app, api, db, jwt


app, api, db, jwt = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=9998)
