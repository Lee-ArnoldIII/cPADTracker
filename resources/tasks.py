import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from models.tasks import TaskModel

class Task(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This field cannot be blank!!.")
    parser.add_argument('description', type=str, required=True, help="This field cannot be blank.")

    
    def get(self, name):
        task = TaskModel.find_by_name(name)
        if task:
            return task.json()
        return {'message': 'Task not found'}, 400

    def post(self, name):
        if TaskModel.find_by_name(name):
            return {"message": "A task with that name already exists."}, 400
        
        data = Task.parser.parse_args()
        
        task = TaskModel(name, **data)
        task.save_to_db()

        return {"message": "Task created successfully."}, 201

    def delete(self, name):
        task = TaskModel.find_by_name(name)
        if task:
            task.delete_from_db()

        return {'message': 'Task deleted'}, 201

    def put(self, name):
        data = Task.parser.parse_args()

        task = TaskModel.find_by_name(name)

        if task is None:
            task = TaskModel(name, **data)
        else:
            task.description = data['description']
        
        task.save_to_db()

        return task.json()


class TaskList(Resource):
    def get(self):
        return {'tasks': [task.json() for task in TaskModel.query.all()]}
        # alternative using lambda => return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}