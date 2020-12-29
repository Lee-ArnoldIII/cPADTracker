from db import db
#TODO: Add following:
# 1) remaining parts of model

# 3) update json function

class ReportModel(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    benchmark = db.Column(db.String(80))
    content = db.Column(db.Text)
    status = db.Column(db.String(80))
    
        
    def __init__(self, name, benchmark, content, status):
        self.name = name
        self.benchmark = benchmark
        self.content = content
        self.status = status
        
     
    def json(self):
        return {'name': self.name, 'benchmark': self.benchmark,'content': self.content, 
                'status': self.status}
        # may need to do a list comprehension for this function to show all reports for a selected user

   
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()