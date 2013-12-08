from google.appengine.ext import ndb


class PricingHistory(ndb.Model):
    recorded_at = ndb.DateTimeProperty()
    usd_price = ndb.FloatProperty()
    volume = ndb.FloatProperty()
