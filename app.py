from flask import Flask, render_template, request, session
from flask_restful import Api
from resources.home import Home
from resources.admin import Admin
from resources.operation import Operation
from resources.book import Book
from resources.finishedbook import Finished
from resources.allusd import Allusd
from models.positionmodel import OperationModel, BookModel, FinishedBookModel, User
import pandas as pd
import bandymeliai
from datetime import datetime

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
def home():
    return render_template('login.html')



@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    password = request.form['password']
    if request.form['submit'] == 'login':
        user = User.find_by_name(name)
        if user is not None and user.password == password and user.name != 'skirma':
            bandymeliai.update_current()
            bookdata = pd.read_sql('book', 'sqlite:///data.db')
            bookdata = bookdata.set_index('id')
            return render_template('main.html', table=bookdata.to_html())
        elif user is not None and user.password == password and user.name == 'skirma':
            return render_template('choose.html')
        else:
            return render_template('login.html')
    elif request.form['submit'] == 'signin':
            name = request.form['name']
            password = request.form['password']
            if name == 'skirma' or name == 'vladas' or name == 'faustas':
                user = User(name, password)
                user.save_to_db()
                bandymeliai.update_current()
                bookdata = pd.read_sql('book', 'sqlite:///data.db')
                bookdata = bookdata.set_index('id')
                return render_template('login.html')
            else:
                return 'Wrong name, please try again'

@app.route('/choose', methods = ['GET', 'POST'])
def choose():
    if request.form['submit'] == 'view':
        bandymeliai.update_current()
        bookdata = pd.read_sql('book', 'sqlite:///data.db')
        bookdata = bookdata.set_index('id')
        return render_template('main.html', table=bookdata.to_html())
    elif request.form['submit'] == 'admin':
        return render_template('admin.html')





@app.route('/admin', methods = ['POST'])
def admin_action():
    name = request.form['crypto_name']
    buy = True
    amount = float(request.form['crypto_amount'])
    price = float(request.form['crypto_price'])
    if request.form['date'] != '':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
    else:
        date = datetime.now()
    position = BookModel.find_by_name(name)
    print(type(amount))
    print(type(price))
    print(type(date))
    if request.form.get('buy_check'):
        if position is not None:
            position.amount = position.amount + amount
            position.total = position.total + (amount*price)
            position.average_price = position.total/position.amount
            position.save_to_db()
            operation = OperationModel(name, amount, price, buy, date)
            operation.save_to_db()
            return render_template("admin.html")
        else:
            position = BookModel(name, amount, price)
            position.save_to_db()
            operation = OperationModel(name, amount, price, buy, date)
            operation.save_to_db()
            return render_template("admin.html")
    elif request.form.get('sell_check'):
        buy = False
        if position is not None:
            if position.amount - amount != 0:
                position.amount = position.amount - amount
                position.total = position.amount * position.average_price
                position.average_price = position.total/position.amount
                position.save_to_db()
                operation = OperationModel(name, amount, price, buy, date)
                operation.save_to_db()
                finish = FinishedBookModel(name, amount, price, date)
                finish.realized_usd = (amount*price) - (position.average_price * amount)
                finish.realized_per = ((price - position.average_price)/position.average_price*100)
                finish.save_to_db()
                return render_template("admin.html")
            else:
                operation = OperationModel(name, amount, price, buy, date)
                operation.save_to_db()
                finish = FinishedBookModel(name, amount, price, date)
                finish.realized_usd = (amount*price) - (position.average_price * amount)
                finish.realized_per = ((price - position.average_price)/position.average_price*100)
                finish.save_to_db()
                position.delete_position()
                return render_template("admin.html")
    else:
        return 'nothing checked you stupid'

@app.route('/pasirinkimas', methods=['POST'])
def pasirinkimas():
    if request.form['submit'] == 'operations':
        operdata = pd.read_sql('operations', 'sqlite:///data.db')
        operdata['time']=operdata['time'].dt.strftime('%Y/%m/%d %H:%M')
        operdata = operdata.iloc[::-1]
        operdata = operdata.set_index('id')
        return render_template('operations.html', table1=operdata.to_html())
    elif request.form['submit'] == 'realized_positions':
        finishdata = pd.read_sql('finishedbook', 'sqlite:///data.db')
        finishdata['time'] = finishdata['time'].dt.strftime('%Y/%m/%d %H:%M')
        finishdata = finishdata.iloc[::-1]
        finishdata = finishdata.set_index('id')
        return render_template('realized.html', table2=finishdata.to_html())





@app.before_first_request
def create_tables():
    db.create_all()



# api.add_resource(Home, '/home')
# api.add_resource(Admin, '/admin')
# api.add_resource(Operation, '/home')
# api.add_resource(Book, '/book')
# api.add_resource(Finished, '/finished')
# api.add_resource(Allusd, '/allusd')
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
