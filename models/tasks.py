import sqlite3
from db import db

class TaskModel(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255))

        

    def __init__(self, task):
       self.task = task
        
    def json(self):
        return {'Task id': self.id, 'Task': self.task}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_task(cls, task):
        return cls.query.filter_by(task=task).first()