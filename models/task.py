import sqlite3
from db import db

class TaskModel(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

    def __init__(self, name, description):
       self.name = name
       self.description = description
        
    def json(self):
        return {'task id': self.id, 'name': self.name, 'description': self.description}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()