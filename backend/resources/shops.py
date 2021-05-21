from flask_restful import Resource
from flask_jwt import jwt_required

from backend.models.shops import StoreModel
from backend.models.items import Item


class Store(Resource):
    @jwt_required()
    def get(self, name):
        shop = StoreModel.get_shop(name)
        if not shop:
            return {'message': f"shop [{name}] doesn't exist"}, 404
        items = Item.get_shop_items(shop)
        return {'name': name, 'items': [{'name': item.name, 'price': item.price} for item in items]}

    @jwt_required()
    def post(self, name):
        if StoreModel.get_shop(name):
            return {'message': f"shop [{name}] already exists"}, 400

        shop = StoreModel(name=name)
        shop.add_shop()
        return {'name': name}, 201

    @jwt_required()
    def delete(self, name):
        shop = StoreModel.get_shop(name)

        if not shop:
            return {'message': f"shop [{name}] doesn't exist"}, 404

        items = Item.get_shop_items(shop)
        for i in items:
            i.delete_item()
        shop.delete_shop()

        return {}, 204


class StoreList(Resource):
    @jwt_required()
    def get(self):
        stores = [(store.name, Item.get_shop_items(store)) for store in StoreModel.get_shops()]
        return {'stores': [{'name': name, 'items': [{'name': item.name, 'price': item.price} for item in items]}
                for name, items in stores]}
