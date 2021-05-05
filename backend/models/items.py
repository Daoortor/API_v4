from backend.db import db


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    price = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return f'<Item {self.name}>'

    @staticmethod
    def get_item(name):
        item = Item.query.filter(Item.name == name).first()
        return item

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
        db.session.query(Item).delete()
        db.session.commit()
