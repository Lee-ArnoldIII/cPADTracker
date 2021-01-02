from db import db
#TODO: Add following:

class ReportModel(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    benchmark = db.Column(db.String(80))
    content = db.Column(db.Text)
    status = db.Column(db.String(80))

    username = db.Column(db.String(80), db.ForeignKey('users.username'))
    users = db.relationship('UserModel')
    
        
    def __init__(self, name, benchmark, content, status, username):
        self.name = name
        self.benchmark = benchmark
        self.content = content
        self.status = status
        self.username = username
        
    def json(self):
        return {'name': self.name, 'benchmark': self.benchmark, 
                'content': self.content, 'status': self.status, 'user': self.username}
   
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()