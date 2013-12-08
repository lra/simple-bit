import json
import time
import datetime
import logging
import forex
import models
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
        timestamp = int(time.mktime(datetime.datetime.utcnow().timetuple()))
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
        self._last_saved = models.PricingHistory.query().order(-models.PricingHistory.recorded_at).get()

    def fetch(self):
        if not self._last_saved or self.age() > 60:
            mtgox = Mtgox()
            bitstamp = Bitstamp()
            btcchina = Btcchina()
            btce = Btce()

            ts_recorded_at = max(mtgox.timestamp,
                                 bitstamp.timestamp,
                                 btcchina.timestamp,
                                 btce.timestamp)
            recorded_at = datetime.datetime.fromtimestamp(ts_recorded_at)

            volume = (mtgox.volume +
                      bitstamp.volume +
                      btcchina.volume +
                      btce.volume)

            usd_price = ((mtgox.usd_price * mtgox.volume
                          + bitstamp.usd_price * bitstamp.volume
                          + btcchina.usd_price * btcchina.volume
                          + btce.usd_price * btce.volume)
                         / volume)

            new_hist = models.PricingHistory(recorded_at=recorded_at,
                                             volume=volume,
                                             usd_price=usd_price)
            new_hist.put()

    def usd_price(self):
        return self._last_saved.usd_price

    def volume(self):
        return self._last_saved.volume

    def recorded_at(self):
        return self._last_saved.recorded_at

    def age(self):
        timedelta = datetime.datetime.utcnow() - self.recorded_at()

        return timedelta.seconds
