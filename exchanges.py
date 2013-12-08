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


class Btce(object):

    def __init__(self):
        self.ticker_url = 'https://btc-e.com/api/2/btc_usd/ticker'
        self._fetch_ticker_data()

    def _fetch_ticker_data(self):
        result = urlfetch.fetch(self.ticker_url)
        if result.status_code == 200:
            str_data = result.content
            self.ticker_data = json.loads(str_data)

    @property
    def usd_price(self):
        price = float(self.ticker_data['ticker']['last'])
        return price

    @property
    def volume(self):
        volume = float(self.ticker_data['ticker']['vol_cur'])
        return volume

    @property
    def timestamp(self):
        timestamp = int(self.ticker_data['ticker']['updated'])
        return timestamp


class Metaex(object):

    def __init__(self):
        self.mtgox = Mtgox()
        self.bitstamp = Bitstamp()
        self.btcchina = Btcchina()
        self.btce = Btce()

    @property
    def usd_price(self):
        return ((self.mtgox.usd_price * self.mtgox.volume
                 + self.bitstamp.usd_price * self.bitstamp.volume
                 + self.btcchina.usd_price * self.btcchina.volume
                 + self.btce.usd_price * self.btce.volume)
                / self.volume)

    @property
    def volume(self):
        return (self.mtgox.volume +
                self.bitstamp.volume +
                self.btcchina.volume +
                self.btce.volume)

    @property
    def timestamp(self):
        return max(self.mtgox.timestamp,
                   self.bitstamp.timestamp,
                   self.btcchina.timestamp,
                   self.btce.timestamp)
