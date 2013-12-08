import webapp2
import exchanges


class MainPage(webapp2.RequestHandler):
    def get(self):
        mtgox = exchanges.Mtgox()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('USD Price: ' + str(mtgox.usd_price))
        self.response.out.write('Volume: ' + str(mtgox.volume))
        self.response.out.write('Timestamp: ' + str(mtgox.timestamp))


routes = [('/', MainPage)]

application = webapp2.WSGIApplication(routes=routes,
                                      debug=True)
