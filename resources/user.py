import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be blank.")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")
    parser.add_argument('user_type', type=str, required=True, help="This field cannot be blank.")
    parser.add_argument('first_name', type=str, required=True, help="This field cannot be blank.")
    parser.add_argument('last_name', type=str, required=True, help="This field cannot be blank.")


    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'], data['user_type'], data['first_name'], data['last_name'] )
        user.save_to_db()

        return {"message": "Candidate created successfully."}, 201

class UserList(Resource):
    def get(self):
        return {'users': [user.json() for user in UserModel.query.all()]}
        # alternative using lambda => return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}