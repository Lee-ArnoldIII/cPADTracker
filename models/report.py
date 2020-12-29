from db import db

class ReportModel(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    date = db.Column(db.Date)

    #TODO: change this later to connect to users table task maybe
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id))
    #user = db.relationship('UserModel')

    def __init__(self, content, date):
        self.content = content
        self.date = date

    def json(self):
        return {'content': self.content, 'date': self.date}

    @classmethod
    def find_by_date(cls, date):
        return cls.query.filter_by(date=date).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    