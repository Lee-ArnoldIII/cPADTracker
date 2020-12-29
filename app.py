from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS
from db import db

from security import authenticate, identity
from resources.user import UserRegister, UserList, User
from resources.task import Task, TaskList
from resources.report import Report, ReportList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
config = {
    'ORIGINS': [
    'http://localhost:3000',  # React
  ],

  'SECRET_KEY': '...'
}

app.secret_key = 'cpanel'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(Report, '/report/<string:name>')
api.add_resource(Task, '/task/<string:name>')
api.add_resource(TaskList, '/tasks')
api.add_resource(ReportList, '/reports')

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<string:username>')
api.add_resource(UserList, '/users')

CORS(app, resources={ r'/*': {'origins': config['ORIGINS']}}, supports_credentials=True)

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)