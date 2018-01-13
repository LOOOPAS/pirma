from flask_restful import Resource, reqparse
from flask import request
from models.positionmodel import OperationModel, BookModel, FinishedBookModel
from models.positionmodel import db



class Admin(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='this field cannot be blank!')
    parser.add_argument('amount', type=float, required=True, help='this field cannot be blank!')
    parser.add_argument('price', type=float, required=True, help='this field cannot be blank!')
    parser.add_argument('buy', type=bool, required=True, help='this field cannot be blank!')

    def get(self):
        pass



    def post(self):
        data = Admin.parser.parse_args()
        print(data)
        position = Position.find_by_name(data['name'])

        if position:
            return {'message':'Position already exists, please update current position'}

        position = Position(data['name'], data['amount'], data['price'])
        position.save_to_db()
        operation = OperationModel(**data)
        operation.save_to_db()
        book = BookModel(data['name'], data['amount'], data['price'], data['price'])
        book.save_to_db()
        return position.json()




    def delete(self):
        data = Admin.parser.parse_args()
        position = Position.find_by_name(data['name'])
        book = BookModel.find_by_name(data['name'])
        if position:
            if position.amount - data['amount'] != 0:
                position.amount = position.amount - data['amount']
                position.total = position.amount*position.price
                position.save_to_db()
                finbook = FinishedBookModel(data['name'],data['amount'],data['price'])
                finbook.realized_usd = (data['amount']*data['price'] -  book.average_price*data['amount'])
                finbook.realized_per = ((data['price'] - book.average_price)/book.average_price)*100
                finbook.save_to_db()
                book.amount = book.amount - data['amount']
                book.total = book.amount*book.average_price
                book.unrealized_usd = (book.amount*book.current_price) - book.total
                book.unrealized_per = ((((book.amount*book.current_price)) - book.total)/book.total)*100
                book.save_to_db()
                operation = OperationModel(**data)
                operation.save_to_db()
                return {'message':'{} have been partially sold'.format(data['name'])}
            position.delete_from_db()
            finbook = FinishedBookModel(data['name'],data['amount'],data['price'])
            finbook.realized_usd = (data['amount']*data['price'] -  book.average_price*data['amount'])
            finbook.realized_per = ((data['price'] - book.average_price)/book.average_price)*100
            finbook.save_to_db()
            book.amount = 0
            book.total = 0
            book.average_price = 0
            book.unrealized_usd = 0
            book.unrealized_per = 0
            book.save_to_db()
            operation = OperationModel(**data)
            operation.save_to_db()

            return {'message':'{} have been sold'.format(data['name'])}
        return {'message':'unable to sell such position does not exist'}



    def put(self):
        data = Admin.parser.parse_args()
        position = Position.find_by_name(data['name'])
        book = BookModel.find_by_name(data['name'])
        if position:
            position.amount = data['amount']
            position.total = position.amount*position.price
            position.save_to_db()
            book.amount = book.amount + data['amount']
            book.total = book.total + (data['amount']*data['price'])
            book.average_price = book.total/book.amount
            book.unrealized_usd = (book.amount*book.current_price) - book.total
            book.unrealized_per = ((((book.amount*book.current_price)) - book.total)/book.total)*100
            book.save_to_db()
            operation = OperationModel(**data)
            operation.save_to_db()
            return {'message':'{} have been increase'.format(data['name'])}
        position = Position(data['name'], data['amount'], data['price'])
        position.save_to_db()
        operation = OperationModel(**data)
        operation.save_to_db()
        book = BookModel(data['name'], data['amount'], data['price'], data['price'])
        book.save_to_db()
        return position.json()
