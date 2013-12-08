import webapp2
import views


routes = [('/', views.IndexPage)]

app = webapp2.WSGIApplication(routes=routes, debug=True)
