from db import db
#TODO: Add following:
# 1) remaining parts of model
# 2) delete from db function
# 3) update json function

class ReportModel(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    benchmark = db.Column(db.String(80))
    content = db.Column(db.Text)
    status = db.Column(db.String(80))
    
        
    def __init__(self, benchmark, content, status):
        self.benchmark = benchmark
        self.content = content
        self.status = status
        
     
    def json(self):
        return {'benchmark': self.benchmark,'content': self.content, 
                'status': self.status}
        # may need to do a list comprehension for this function to show all reports for a selected user

   
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()