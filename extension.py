import requests
import json
from config import API_KEY

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(quote,base,amount):
        if base == quote:
            raise APIException('Нельзя конвертировать одинаковые валюты')

        url = "https://api.apilayer.com/exchangerates_data/convert"
        headers = {
            "apikey": API_KEY
        }
        params = {
            "to": quote,
            "from": base,
            "amount": amount
        }
        r = requests.get(url, headers=headers, params=params)

        data = json.loads(r.text)

        if 'result' not in data:
            raise APIException('Сбой в матрице\n'
                               'Попробуй снова')
        return round(data['result'])