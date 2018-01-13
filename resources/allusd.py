from flask_restful import Resource, reqparse
from flask import request
from models.positionmodel import FinishedBookModel
import json

class Allusd(Resource):
    def get(self):
        finish = FinishedBookModel.query.all()
        suma = 0
        for x in finish:
            suma += x.realized_usd
        return {'message':'total realized gain in usd {}'.format(suma)}
