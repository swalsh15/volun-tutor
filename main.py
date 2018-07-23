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
        template = env.get_template('/templates/index.html')
        self.response.write(template.render())

class SignUp(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('/templates/signup.html')
        self.response.write(template.render())
    def post(self):
        name = self.request.get('username')
        type = self.request.get('type')

        new_user = User(name = name, type = type)
        new_user.put()

        template = env.get_template('/templates/view_posts.html')

class User(ndb.Model):
    name = ndb.StringProperty()
    type = ndb.StringProperty()

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/join', SignUp),

], debug=True)
