from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from models.task import TaskModel

class Task(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('description', 
        type=str,
        required=True,
        help="This field cannot be blank!"
    )

    @jwt_required()
    def get(self, name):
        task = TaskModel.find_by_name(name)
        if task:
            return task.json()
        return {'message': "Task not found!"}, 404

    def post(self, name):
        if TaskModel.find_by_name(name):
            return {'message': f"A task with name '{name}' already exists!"}, 400
        
        data = Task.parser.parse_args()

        task = TaskModel(name, **data)

        try:
            task.save_to_db()
        except:
            return {'message': "An error occured creating the task."}, 500

        return task.json()

    def delete(self, name):
        task = TaskModel.find_by_name(name)
        if task is None:
            return {'message': 'Task not found!'}, 404
        else:
            task.delete_from_db()
            return {'message': 'Task deleted.'}

    def put(self, name):
        data = Task.parser.parse_args()

        task = TaskModel.find_by_name(name)

        if task is None:
            task = TaskModel(name, **data)
        else: 
            task.name = name
            task.description = data['description']
        
        try:
            task.save_to_db()
        except:
            return {'message': "An error occured."}, 500
        
        return task.json()


class TaskList(Resource):
    def get(self):
        return {'tasks': [task.json() for task in TaskModel.query.all()]}