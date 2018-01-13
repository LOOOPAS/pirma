from flask_restful import Resource, reqparse
from models.positionmodel import OperationModel
from flask import render_template
import pandas as pd


class Home(Resource):
    def get(self):
        data = pd.read_sql('operations', 'sqlite:///data.db')
        return render_template('index.html')
