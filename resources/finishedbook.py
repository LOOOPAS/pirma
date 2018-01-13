from flask_restful import Resource, reqparse
from flask import request
from models.positionmodel import FinishedBookModel


class Finished(Resource):
    def get(self):
        return {'Operation ROI':[x.json() for x in FinishedBookModel.query.all()]}
