import json
import time
import forex
from google.appengine.api import urlfetch


class Mtgox(object):

    def __init__(self):
        self.ticker_url = 'http://data.mtgox.com/api/2/BTCUSD/money/ticker'
        self._fetch_ticker_data()

    def _fetch_ticker_data(self):
        result = urlfetch.fetch(self.ticker_url)
        if result.status_code == 200:
            str_data = result.content
            json_data = json.loads(str_data)
            if json_data.get('result') == 'success':
                self.ticker_data = json_data

    @property
    def usd_price(self):
        price = float(self.ticker_data['data']['last_all']['value'])
        return price

    @property
    def volume(self):
        volume = float(self.ticker_data['data']['vol']['value'])
        return volume

    @property
    def timestamp(self):
        timestamp = int(float(self.ticker_data['data']['now']) / 1000000)
        return timestamp


class Bitstamp(object):

    def __init__(self):
        self.ticker_url = 'http://www.bitstamp.net/api/ticker/'
        self._fetch_ticker_data()

    def _fetch_ticker_data(self):
        result = urlfetch.fetch(self.ticker_url)
        if result.status_code == 200:
            str_data = result.content
            self.ticker_data = json.loads(str_data)

    @property
    def usd_price(self):
        price = float(self.ticker_data['last'])
        return price

    @property
    def volume(self):
        volume = float(self.ticker_data['volume'])
        return volume

    @property
    def timestamp(self):
        timestamp = int(self.ticker_data['timestamp'])
        return timestamp


class Btcchina(object):

    def __init__(self):
        self.ticker_url = 'http://data.btcchina.com/data/ticker'
        self._fetch_ticker_data()

    def _fetch_ticker_data(self):
        result = urlfetch.fetch(self.ticker_url)
        if result.status_code == 200:
            str_data = result.content
            self.ticker_data = json.loads(str_data)

    @property
    def cny_price(self):
        price = float(self.ticker_data['ticker']['last'])
        return price

    @property
    def usd_price(self):
        fx = forex.Forex()
        price = fx.from_cny_to_usd(self.cny_price)
        return price

    @property
    def volume(self):
        volume = float(self.ticker_data['ticker']['vol'])
        return volume

    @property
    def timestamp(self):
        timestamp = int(time.time())
        return timestamp
