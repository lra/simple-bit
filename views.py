import os
import jinja2
import webapp2
import exchanges


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))


class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(self, filename, template_values, **template_args):
        template = JINJA_ENVIRONMENT.get_template(filename)
        self.response.out.write(template.render(template_values))


class IndexPage(BaseHandler):

    def get(self):
        mtgox = exchanges.Mtgox()
        bitstamp = exchanges.Bitstamp()
        btcchina = exchanges.Btcchina()
        btce = exchanges.Btce()
        variables = {
            'mtgox': mtgox,
            'bitstamp': bitstamp,
            'btcchina': btcchina,
            'btce': btce,
        }
        self.render_template('index.html', variables)
