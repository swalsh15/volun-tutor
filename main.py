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

        new_user = User(
        name = self.request.get('username'),
        type = self.request.get('type'),
        email = self.request.get('email'),
        password = self.request.get('password'),
        zipcode = self.request.get('zipcode'),


        )
        new_user.put()

        template = env.get_template('/templates/view_posts.html')
        self.response.write(template.render())

class ViewPosts(webapp2.RequestHandler):
    def get(self):
        template =env.get_template('/templates/view_posts.html')
        self.response.write(template.render())

class Login(webapp2.RequestHandler):
    def get(self):
        template =env.get_template('/templates/login.html')
        self.response.write(template.render())

class User(ndb.Model):
    name = ndb.StringProperty()
    type = ndb.StringProperty()
    zipcode = ndb.IntegerProperty()
    grade = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/join', SignUp),
    ('/view_posts', ViewPosts),
    ('/login', Login),
], debug=True)
