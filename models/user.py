import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    user_type = db.Column(db.String(80))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
        

    def __init__(self, username, password, user_type, first_name, last_name):
       self.username = username
       self.password = password
       self.user_type = user_type
       self.first_name = first_name
       self.last_name = last_name
        
    def json(self):
        return {'User': self.id, 'Username': self.username, 'First Name': self.first_name, 'Last Name': self.last_name, 'User Type': self.user_type}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, __id):
        return cls.query.filter_by(id=_id).first()