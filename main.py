import webapp2
import views


routes = [
    ('/', views.IndexPage),
    ('/fetch', views.FetchPage),
]

app = webapp2.WSGIApplication(routes=routes, debug=True)
