from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from models.report import ReportModel


#TODO: Add following:
# 1) parser arguments from model
# 2) all CRUD methods
# 3) test to make sure this doesn't jack up JWT

class Report(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('benchmark', 
            type=str,
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('content', 
            type=str,
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('status', 
            type=str,
            required=True,
            help="This field cannot be blank!"
    )

    @jwt_required()
    def get(self, id):
        report = ReportModel.find_by_id(id)
        if report:
            return report.json()
        return {'message': 'Report not found!'}, 404

    def post(self, id):
        if ReportModel.find_by_id(id):
            return {'message': "That report already exists!"}, 400
        
        data = Report.parser.parse_args()

        report = ReportModel(id, **data)

        try:
            report.save_to_db()
        except:
            return {'message': "An error occured creating the task."}, 500

        return report.json()

    # def delete(self, name):
    #     task = TaskModel.find_by_name(name)
    #     if task is None:
    #         return {'message': 'Task not found!'}, 404
    #     else:
    #         task.delete_from_db()
    #         return {'message': 'Task deleted.'}

    # def put(self, name):
    #     data = Task.parser.parse_args()

    #     task = TaskModel.find_by_name(name)

    #     if task is None:
    #         task = TaskModel(name, **data)
    #     else: 
    #         task.name = name
    #         task.description = data['description']
        
    #     try:
    #         task.save_to_db()
    #     except:
    #         return {'message': "An error occured."}, 500
        
    #     return task.json()


class ReportList(Resource):
    def get(self):
        return {'report': [report.json() for report in ReportModel.query.all()]}