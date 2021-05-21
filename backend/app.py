import os

import sqlite3
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from backend.security import authenticate, identity
from backend.resources.items import ItemResource, ItemList
from backend.resources.users import UserResource
from backend.resources.shops import Store, StoreList
from confidential import SECRET_KEY, ADMIN
from backend.db import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.dirname(os.path.realpath(__file__))}//data.db'
    db.init_app(app)
    # with app.app_context():
    #     db.create_all()
    # db.session.commit()
    api = Api(app)

    app.config['SECRET_KEY'] = SECRET_KEY
    jwt = JWT(app, authenticate, identity)

    api.add_resource(ItemResource, '/items/<string:name>')
    api.add_resource(ItemList, '/items')
    api.add_resource(UserResource, '/register')
    api.add_resource(Store, '/stores/<string:name>')
    api.add_resource(StoreList, '/stores')

    return app, api, jwt


app, api, jwt = create_app()

ADMIN = eval(ADMIN)


@app.before_first_request
def create():
    with app.app_context():
        db.create_all()

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    create_admin = f'INSERT OR IGNORE INTO users (username, password) VALUES ("{ADMIN["username"]}", "{ADMIN["password"]}")'
    cursor.execute(create_admin)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    # create()
    app.run(debug=True, port=9998)
