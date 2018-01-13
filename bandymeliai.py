import requests
from models.positionmodel import BookModel




def update_current():
    content=requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=0')
    content=content.json()
    for i in content:
        position = BookModel.find_by_name(i['symbol'].lower())

        if position is not None:
            position.current_price = float(i['price_usd'])
            position.unrealized_usd = (position.amount * position.current_price) - position.total
            position.unrealized_per = (((position.amount * position.current_price) - position.total)/position.total)*100
            position.save_to_db()
