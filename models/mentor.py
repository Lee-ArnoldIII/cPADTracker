from db import db

class MentorModel(db.Model):
    __tablename__ = 'mentors'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))

    users = db.relationship('UserModel', lazy='dynamic')

    def __init__(self, username, password, first_name, last_name):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name


    def json(self):
        return {'username': self.username, 'first_name': self.first_name, 'last_name': self.last_name}

    def json2(self):
        return {'user': self.username, 'mentees': [users.json() for users in self.users.all()]}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()