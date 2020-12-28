from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from models.task import TaskModel

class TaskRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', 
            type=str, 
            required=True, 
            help="This field cannot be blank!"
    )
    parser.add_argument('description', 
            type=str, 
            required=True, 
            help="This field cannot be blank!"
    )

    # @jwt_required()
    def get(self, name):
        task = TaskModel.find_by_name(name)
        if task:
            return task.json()
        return {"message": "Task not found"}, 404

    def post(self, name):
        if TaskModel.find_by_name(name):
            return {"message": "A task with that name already exists"}, 400

        data = TaskRegister.parser.parse_args()

        task = TaskModel(**data)
        task.save_to_db()

        return {"message": "Task created successfully."}, 201

    def delete(self, name):
        task = TaskModel.find_by_name(name)
        if task:
            task.delete_from_db()
        
        return {'message': 'Task deleted.'}

    def put(self, name):
        data = TaskRegister.parser.parse_args()

        task = TaskModel.find_by_name(name)

        if task is None:
            task = TaskModel(**data)
        else:
            task.name = data['name']
            task.description = data['description']
        
        task.save_to_db()

        return task.json()

    
class TaskList(Resource):
    def get(self):
        return {'tasks': [task.json() for task in TaskModel.query.all()]}
        # alternative using lambda => return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}