from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required

from backend.models.items import Item
from backend.models.shops import StoreModel


class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'shop_name',
        type=str,
        required=True,
        help="Invalid shop name")

    @jwt_required()
    def get(self, name):
        shop_name = ItemResource.parser.parse_args()['shop_name']
        shop = StoreModel.get_shop(shop_name)
        item = Item.get_item(name, shop)
        if not item:
            return {'message': f"item [{name}] doesn't exist in the shop [{shop_name}]"}, 404
        return {'name': item.name, 'price': item.price}, 200

    @jwt_required()
    def post(self, name):
        ItemResource.parser.add_argument('price', type=int, required=True, help='Invalid price value')
        price = ItemResource.parser.parse_args()['price']
        shop_name = ItemResource.parser.parse_args()['shop_name']
        ItemResource.parser.remove_argument('price')
        shop = StoreModel.get_shop(shop_name)

        if not shop:
            return {'message': f"shop [{shop_name}] doesn't exist"}, 404
        if Item.get_item(name, shop):
            return {'message': f"item [{name}] already exists"}, 400

        item = Item(name=name, price=price, shop_id=shop.id)
        item.add_item()
        return {'name': name, 'price': price, 'shop_name': shop_name}, 201

    @jwt_required()
    def put(self, name):
        ItemResource.parser.add_argument('price', type=int, required=True, help='Invalid price value')
        price = ItemResource.parser.parse_args()['price']
        shop_name = ItemResource.parser.parse_args()['shop_name']
        ItemResource.parser.remove_argument('price')
        shop = StoreModel.get_shop(shop_name)

        if not shop:
            return {'message': f"shop [{shop_name}] doesn't exist"}, 404
        if not Item.get_item(name, shop):
            item = Item(name=name, price=price, shop_id=shop.id)
            item.add_item()
            return {'name': name, 'price': price, 'shop_name': shop_name}, 201
        Item.change_item(name, price)
        return {'name': name, 'price': price, 'shop_name': shop_name}, 200

    @jwt_required()
    def delete(self, name):
        shop_name = ItemResource.parser.parse_args()['shop_name']
        shop = StoreModel.get_shop(shop_name)
        item = Item.get_item(name, shop)
        if not item:
            return {'message': f"item {name} doesn't exist"}, 404
        item.delete_item()
        return {}, 204


class ItemList(Resource):
    @jwt_required()
    def get(self):
        items = Item.get_items()
        return {'items': [{'name': item.name, 'price': item.price} for item in items]}

    @jwt_required()
    def post(self):
        json = request.get_json()
        shop_name = json['shop_name']
        items = json['items']
        shop = StoreModel.get_shop(shop_name)
        bad_item_names = []
        for item in items:
            existing_item = Item.get_item(item['name'], shop)
            if existing_item:
                bad_item_names.append(existing_item['name'])
        if bad_item_names:
            return {'message': f'items {bad_item_names} already exist'}, 400

        for item in items:
            new_item = Item(name=item['name'], price=item['price'], shop_id=shop.id)
            new_item.add_item()
        return {'items': items}, 201

    @jwt_required()
    def delete(self):
        if not Item.get_items():
            return {'message': f'There are no items in the store'}, 400
        Item.delete_items()
        return {}, 204
