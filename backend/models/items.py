from backend.db import db


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    shop_id = db.Column(db.Integer(), db.ForeignKey('shops.id'))

    def __repr__(self):
        return f'<Item {self.name}>'

    @staticmethod
    def get_item(name, shop):
        item = Item.query.filter(Item.name == name, Item.shop_id == shop.id).all()
        if item:
            return item[0]
        return None

    def add_item(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def change_item(name, price):
        db.session.query(Item).filter(Item.name == name).update({'price': price})
        db.session.commit()

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_items():
        return Item.query.all()

    @staticmethod
    def delete_items():
        Item.query.delete()
        db.session.commit()

    @staticmethod
    def get_shop_items(shop):
        return Item.query.filter(Item.shop_id == shop.id).all()

    @staticmethod
    def delete_shop_items(shop):
        Item.query.filter(Item.shop_id == shop.id).delete()
        db.session.commit()
