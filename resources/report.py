from flask_jwt import JWT, jwt_required
from flask_restful import Resource, reqparse
from models.report import ReportModel

class Report(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('benchmark', 
            type=str,
            help="This cannot be blank!"
    )
    parser.add_argument('content', 
            type=str,
            help="This cannot be blank!"
    )
    parser.add_argument('status', 
            type=str,
            help="This cannot be blank!"
    )

    @jwt_required()
    def get(self, name):
        report = ReportModel.find_by_name(name)
        if report:
            return report.json()
        return {'message': "Report not found!"}, 404

    def post(self, name):
        if ReportModel.find_by_name(name):
            return {'message': "A report with that id already exists!"}, 400
        
        data = Report.parser.parse_args()

        report = ReportModel(name, **data)

        try:
            report.save_to_db()
        except: 
            return {'message': "An error occured creating the report!"}, 500

        return {'message': "Report created successfully."}, 201

    def put(self, name):
        pass

    def delete(self, name):
        pass


class ReportList(Resource):
    def get(self):
        return {'reports': [report.json() for report in ReportModel.query.all()]}