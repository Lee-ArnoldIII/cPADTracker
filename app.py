from db import db
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identify
from resources.user import UserRegister, UserList
from resources.tasks import TaskRegister, TaskList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cpanel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'cpanel1'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identify)

api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')
api.add_resource(TaskRegister, '/taskregister')
api.add_resource(TaskList, '/tasks')
# api.add_resource(<name>, '/<routeName>')

# api.add_resource(<name>, '/<routeName>')
# api.add_resource(<name>, '/<routeName>')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)