from flask_restful import Resource, reqparse
from flask import request
from models.positionmodel import OperationModel


class Operation(Resource):
    def get(self):
        print({'operations':[x.json() for x in OperationModel.query.all()]})
        return {'operations':[x.json() for x in OperationModel.query.all()]}
