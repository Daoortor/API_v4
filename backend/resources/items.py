from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required

from backend.models.items import Item


class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="Invalid value for price"
    )

    @jwt_required()
    def get(self, name):
        item = Item.get_item(name)
        if not item:
            return {'message': f"item [{name}] doesn't exist"}, 404
        return {'name': item.name, 'price': item.price}, 200

    @jwt_required()
    def post(self, name):
        if Item.get_item(name):
            return {'message': f"item [{name}] already exists"}, 400
        price = ItemResource.parser.parse_args()['price']
        item = Item(name=name, price=price)
        item.add_item()
        return {'name': name, 'price': price}, 201

    @jwt_required()
    def put(self, name):
        price = ItemResource.parser.parse_args()['price']
        if not Item.get_item(name):
            item = Item(name=name, price=price)
            item.add_item()
            return {'name': name, 'price': price}, 201
        Item.change_item(name, price)
        return {'name': name, 'price': price}, 200

    @jwt_required()
    def delete(self, name):
        item = Item.get_item(name)
        if not item:
            return {'message': f"item {name} doesn't exist"}, 404
        item.delete_item()
        return {}, 204


class ItemList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'items',
        type=dict,
        action='append'
    )

    @jwt_required()
    def get(self):
        items = Item.get_items()
        return {'items': [{'name': item.name, 'price': item.price} for item in items]}

    @jwt_required()
    def post(self):
        items = request.json['items']
        bad_item_names = []
        for item in items:
            existing_item = Item.get_item(item['name'])
            if existing_item:
                bad_item_names.append(existing_item['name'])
        if bad_item_names:
            return {'message': f'items {bad_item_names} already exist'}, 400

        for item in items:
            new_item = Item(name=item['name'], price=item['price'])
            new_item.add_item()
        return {'items': items}, 201

    @jwt_required()
    def delete(self):
        if not Item.get_items():
            return {'message': f'There are no items in the store'}, 400
        Item.delete_items()
        return {}, 204
