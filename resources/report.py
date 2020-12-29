from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from models.report import ReportModel

class Report(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('content', 
            type=str,
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('date', 
            type=str,
            required=True,
            help="This field cannot be blank!"
    )

    @jwt_required()
    def get(self, date):
        report = ReportModel.find_by_date(date)
        if report:
            return report.json()
        return {'message': 'Report not found!'}, 404


class ReportList(Resource):
    def get(self):
        return {'report': [report.json() for report in ReportModel.query.all()]}