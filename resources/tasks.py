import sqlite3
from flask_restful import Resource, reqparse
from models.tasks import TaskModel

class TaskRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('task', type=str, required=True, help="This field cannot be blank.")

    def post(self):
        data = TaskRegister.parser.parse_args()

        if TaskModel.find_by_task(data['task']):
            return {"message": "A user with that username already exists"}, 400

        task = TaskModel(data['task'])
        task.save_to_db()

        return {"message": "Task created successfully."}, 201

class TaskList(Resource):
    def get(self):
        return {'tasks': [task.json() for task in TaskModel.query.all()]}
        # alternative using lambda => return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}