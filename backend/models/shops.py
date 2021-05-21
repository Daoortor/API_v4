from backend.db import db


class StoreModel(db.Model):
    __tablename__ = 'shops'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    items = db.relationship('Item', backref='store', lazy=True)

    def __repr__(self):
        return f'<Item {self.name}>'

    @staticmethod
    def get_shop(name):
        shop = StoreModel.query.filter(StoreModel.name == name).first()
        return shop

    def add_shop(self):
        db.session.add(self)
        db.session.commit()

    def delete_shop(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_shops():
        return StoreModel.query.all()
