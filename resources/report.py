from flask_jwt import JWT, jwt_required
from flask_restful import reqparse, Resource
from models.report import ReportModel

class Report(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('benchmark', 
            type=str,
            help='This cannot be blank!'
    )
    parser.add_argument('content', 
            type=str,
            required=True,
            help='This cannot be blank!'
    )
    parser.add_argument('status', 
            type=str,
            required=True,
            help='This cannot be blank!'
    )

    @jwt_required()
    def get(self, name):
        report = ReportModel.find_by_name(name)
        if report:
            return report.json()
        return {'message': "Report not found!"}, 404

    def post(self, name):
        if ReportModel.find_by_name(name):
            return {'message': "A report with that name already exists!"}, 400

        data = Report.parser.parse_args()

        report = ReportModel(name, **data)

        try:
            report.save_to_db()
        except:
            return {'message': "An error occured while creating the report."}, 500

        return report.json()
        # return {'message': "Report successfully created."}, 201

    def put(self, name):
        data = Report.parser.parse_args()

        report = ReportModel.find_by_name(name)

        if report is None:
            report = ReportModel(name, **data)
        else: 
            report.benchmark = data['benchmark']
            report.content = data['content']
            report.status = data['status']
           
        try:
            report.save_to_db()
        except:
            return {'message': "An error occured."}, 500

        return report.json()

    def delete(self, name):
        report = ReportModel.find_by_name(name)
        if report is None:
            return {'message': "Report not found!"}, 404
        else:
            report.delete_from_db()
            return {'message': "Report deleted."}

class ReportList(Resource):
    def get(self):
        return {'reports': [report.json() for report in ReportModel.query.all()]}