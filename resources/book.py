from flask_restful import Resource, reqparse
from flask import request
from models.positionmodel import BookModel


class Book(Resource):
    def get(self):
        return {'book':[x.json() for x in BookModel.query.all()]}
