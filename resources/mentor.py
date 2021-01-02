from flask_restful import reqparse, Resource
from flask_jwt import JWT, jwt_required
from models.mentor import MentorModel

class MentorRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
            type=str,
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('password',
            type=str,
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('first_name',
            type=str,
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('last_name',
            type=str,
            required=True,
            help="This field cannot be blank!"
    )

    def post(self):
        data = MentorRegister.parser.parse_args()

        if MentorModel.find_by_username(data['username']):
            return {'message': "Mentor already exists!"},400

        mentor = MentorModel(**data)
        mentor.save_to_db()

        return {'message': "Mentor created successfully."}, 201



class Mentor(Resource):

    @jwt_required()
    def get(self, username):
        mentor = MentorModel.find_by_username(username)
        if mentor: 
            return mentor.json()
        return {'message': "This mentor does not exist!"}, 404

    def put(self, username):
        data = Mentor.parser.parse_args()

        mentor = MentorModel.find_by_username(username)

        if mentor is None:
            mentor = MentorModel(username, **data)
        else:
            mentor.username = username
            mentor.password = data['password']
            mentor.first_name = data['first_name']
            mentor.last_name = data['last_name']
            

        mentor.save_to_db()

        return mentor.json()

    
    def delete(self, username):
        mentor = MentorModel.find_by_username(username)
        if mentor is None:
            return {'message': 'Mentor not found!'}, 404
        else:
            mentor.delete_from_db()
            return {'message': 'Mentor deleted!'}


class MentorList(Resource):
    def get(self):
        return {'Mentors': [mentor.json() for mentor in MentorModel.query.all()]}



class UserMentors(Resource):
    def get(self, username):
        user = MentorModel.find_by_username(username)
        if user:
            return user.json2()
        return {'message': "This mentor has no mentees!"}, 404