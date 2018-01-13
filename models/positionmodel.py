from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from db import db
import json
import requests



class OperationModel(db.Model):
    __tablename__ = 'operations'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    name =  db.Column(db.String(10))
    amount = db.Column(db.Float(precizion=4))
    price = db.Column(db.Float(precizion=4))
    total = db.Column(db.Float(precizion=4))
    buy = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, amount, price, buy, date):
        self.time = date
        self.name = name
        self.amount = amount
        self.price = price
        self.total = amount * price
        self.buy = buy

    def json(self):
        return{'no:':self.id, 'time':self.time.strftime('%Y/%m/%d %H:%M'),
        'name': self.name, 'amount': self.amount,
        'price':self.price, 'total':self.total, 'buy':self.buy}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class BookModel(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(10), unique=True)
    amount = db.Column(db.Float(precizion=4))
    average_price = db.Column(db.Float(precizion=4))
    total = db.Column(db.Float(precizion=4))
    current_price = db.Column(db.Float(precizion=4))
    unrealized_usd = db.Column(db.Float(precizion=4))
    unrealized_per = db.Column(db.Float(precizion=2))

    def __init__(self, name, amount, price):
        self.name = name
        self.amount = amount
        self.average_price = price
        self.total = amount * price
        self.current_price = 0
        self.unrealized_usd = 0
        self.unrealized_per = 0

    def json(self):
        return {'name':self.name, 'amount':self.amount, 'avgprice':self.average_price,
        'total': self.total, 'current price':self.current_price, 'Unrealized gain usd':self.unrealized_usd,
        'Unrealized gain %':self.unrealized_per}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def delete_position(self):
        db.session.delete(self)
        db.session.commit()


class FinishedBookModel(db.Model):
    __tablename__ = 'finishedbook'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    name =  db.Column(db.String(10))
    amount = db.Column(db.Float(precizion=4))
    price = db.Column(db.Float(precizion=4))
    total = db.Column(db.Float(precizion=4))
    realized_usd = db.Column(db.Float(precizion=4))
    realized_per = db.Column(db.Float(precizion=2))


    def __init__(self, name, amount, price, date):
        self.time = date
        self.name = name
        self.amount = amount
        self.price = price
        self.total = self.amount*self.price
        self.realized_usd = 0
        self.realized_per = 0


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {'no':self.id, 'time':self.time.strftime('%Y/%m/%d %H:%M'),'name':self.name, 'amount':self.amount,
        'price':self.price,'total': self.total, 'Realized gain usd':self.realized_usd,
        'Realized gain %':self.realized_per}

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
