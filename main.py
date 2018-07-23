import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import users

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

        user = users.get_current_user()
        #self.response.write(user.user_id())
        #assign these to something so the program runs
        nickname = None
        logout_url = None
        login_url = None

        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
        else:
            login_url = users.create_login_url('/')


        template_vars = {
            "user" : user,
            "nickname" : nickname,
            "logout_url" : logout_url,
            "login_url" : login_url,
        }

        template = env.get_template('/templates/signup.html')
        self.response.write(template.render(template_vars))

class ViewPosts(webapp2.RequestHandler):
    def get(self):
        template =env.get_template('/templates/view_posts.html')
        self.response.write(template.render())


class CreatePost(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            template =env.get_template('/templates/post.html')
            self.response.write(template.render())
    def post(self):
        user = users.get_current_user()
        if user:
            new_post = Post(author = user.user_id(),
            title = self.request.get('title'),
            content = selsf.request.get('post'))
            new_post.put()

            #display posts
            allPosts = Post.query()
            template_vars = {}
            titleList = []
            contentList = []

            for i in allPosts.fetch():
                contentList.append(i.content)
                titleList.append(i.title)

            template_vars['titlelist'] = titleList
            template_vars['contents'] = contentList
            template_vars['length'] = len(titleList)

            template =env.get_template('/templates/view_posts.html')
            self.response.write(template.render(template_vars))

class User(ndb.Model):
    name = ndb.StringProperty()
    type = ndb.StringProperty()
    zipcode = ndb.StringProperty()
    grade = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()

class Post(ndb.Model):
    title = ndb.StringProperty()
    author = ndb.StringProperty()
    content = ndb.StringProperty()

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/join', SignUp),
    ('/view_posts', ViewPosts),
    ('/post', CreatePost)
], debug=True)
