import json
from google.appengine.api import urlfetch


class Forex(object):

    def __init__(self):
        self.ticker_url = 'http://rate-exchange.appspot.com/currency?from=CNY&to=USD'
        self._fetch_data()

    def _fetch_data(self):
        result = urlfetch.fetch(self.ticker_url)
        if result.status_code == 200:
            str_data = result.content
            json_data = json.loads(str_data)
            if json_data.get('rate'):
                self.json_data = json_data

    def from_cny_to_usd(self, cny):
        assert isinstance(cny, float)
        rate = float(self.json_data.get('rate'))
        return cny * rate
