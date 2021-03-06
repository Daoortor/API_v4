from backend.db import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def add_user(self):
        db.session.add(self)
        db.session.commit()

    def remove_user(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def find_by_username(value):
        db.create_all()
        return db.session.query(User).filter_by(username=value).first()

    @staticmethod
    def find_by_id(value):
        db.create_all()
        return db.session.query(User).filter_by(id=value).first()
