import webapp2
import jinja2
import os
from google.appengine.ext import ndb

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("hello world")

app = webapp2.WSGIApplication([
    ('/', MainPage),

], debug=True)
