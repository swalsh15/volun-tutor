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
        user = users.get_current_user()
        current_user = None
        if user != None:
            current_user = User.query(User.id == user.user_id()).get()

        template_vars = {'user': user, 'logout_url': users.create_logout_url('/'), 'current_user' : current_user}
        template = env.get_template('/templates/index.html')
        self.response.write(template.render(template_vars))

class SignUp(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()
        nickname = None
        logout_url = None
        login_url = None

        if user:
            if User.query(User.id == user.user_id()).get():
                self.redirect('/profile')
            else:
                 self.redirect('/create_profile')
        else:
            login_url = users.create_login_url('/')
            self.redirect(login_url)


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
        title = []
        content = []
        authors = []
        author_names = []

        #get current user's type
        user = users.get_current_user()
        current_user = User.query(User.id == user.user_id()).get()
        current_user_type = current_user.type

        #determine what feed to load
        if current_user_type == 'Tutor':
            allPosts = Post.query(Post.type == 'Student')
            feed_name = 'Student Feed'
        else:
            allPosts = Post.query(Post.type == 'Tutor')
            feed_name = 'Tutor Feed'

        for blog_post in allPosts.fetch():
            title.append(blog_post.title)
            content.append(blog_post.content)
            if blog_post.author != None:
                authors.append(blog_post.author)
                author_names.append(blog_post.author.get().name)

        template_vars = {
            'title': title,
            'content': content,
            'length' : len(title),
            'feed_name' : feed_name,
            'author': authors,
            'author_name': author_names
        }
        template = env.get_template('/templates/view_posts.html')
        self.response.write(template.render(template_vars))
    def post(self):
        title = []
        content = []
        key_string = self.request.get('button')
        key = ndb.Key(urlsafe = key_string)

        profile_info = key.get()
        if profile_info.name:
            user_name = profile_info.name
        else:
            user_name = 'ononononon'
        user_posts = profile_info.posts
        for user_post in user_posts:
            title.append(user_post.get().title)
            content.append(user_post.get().content)

        if len(user_name) != 0:
            first_letter = user_name[0].upper()
        else:
            first_letter = ""

        template_vars = {
        'name': user_name,
        'type': profile_info.type,
        'zipcode': profile_info.zipcode,
        'grade': profile_info.grade,
        'length': len(title),
        'title': title,
        'first_letter': first_letter,
        'edit_button' : False,
        'content': content,
        'id': profile_info.id,
        'logout_url' : users.create_logout_url('/'),
        'email': profile_info.email
        }
        template = env.get_template('/templates/profile.html')
        self.response.write(template.render(template_vars))

class CreatePost(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            template_vars = {'logout_url': users.create_logout_url('/')}
            template = env.get_template('/templates/post.html')
            self.response.write(template.render(template_vars))
    def post(self):
        allPosts = Post.query()
        user = users.get_current_user()
        title = self.request.get('title')
        content = self.request.get('post')
        author = User.query(User.id == user.user_id()).get() #returns user object

        if user:
            new_post = Post(type = author.type,
            title = self.request.get('title'),
            content = self.request.get('post'),
            author = author.key,
            author_name = author.name)
            new_post_key= new_post.put()
            author.posts.append(new_post_key)
            author.put()
            profile_info = User.query(User.id == user.user_id()).get()
            profile_type = profile_info.type
            if profile_type == 'Tutor':
                otype = 'Student'
            else:
                otype = 'Tutor'


            template_vars= {
            'title': title,
            'content':content,
            'author': author.name,
            'Opposite_type': otype
            }
            template = env.get_template('/templates/confirmpost.html')
            self.response.write(template.render(template_vars))


class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            template = env.get_template('/templates/create_profile.html')
            self.response.write(template.render())
    def post(self):
        user = users.get_current_user()

        #user variables
        name = self.request.get('name')
        type = self.request.get('type')
        zipcode = self.request.get('zipcode')
        grade = self.request.get('grade')
        id = user.user_id()
        email = user.email()

        new_user = User(name = name,
        type = type,
        zipcode = zipcode,
        grade = grade,
        id = id,
        email = email)
        if len(name) != 0:
            first_letter = name[0].upper()
        else:
            first_letter = ""
        new_user.put()

        template_vars = {
        'name': name,
        'type': type,
        'zipcode': zipcode,
        'grade': grade,
        'length': 0,
        'id': id,
        'logout_url' : users.create_logout_url('/'),
        'first_letter': first_letter,
        'email': email
        }

        template = env.get_template('/templates/profile.html')
        self.response.write(template.render(template_vars))

class ShowProfile(webapp2.RequestHandler):
    def get(self):
        title = []
        content = []
        user = users.get_current_user()
        profile_info = User.query(User.id == user.user_id()).get()
        user_posts = profile_info.posts
        user_name = profile_info.name
        for user_post in user_posts:
            title.append(user_post.get().title)
            content.append(user_post.get().content)

        if len(profile_info.name) != 0:
            first_letter = profile_info.name[0].upper()
        else:
            first_letter = ""

        template_vars = {
        'name': profile_info.name,
        'edit_button': True,
        'first_letter': first_letter,
        'type': profile_info.type,
        'zipcode': profile_info.zipcode,
        'grade': profile_info.grade,
        'length': len(title),
        'title': title,
        'content': content,
        'id': profile_info.id,
        'logout_url' : users.create_logout_url('/'),
        'email': profile_info.email
        }

        template = env.get_template('/templates/profile.html')
        self.response.write(template.render(template_vars))
    def post(self):
        self.redirect('/edit')
        # user = users.get_current_user()
        # profile = self.request.get('edit')
        # current_user = User.query(User.name == profile).get()
        #
        # #so user can't change other profiles
        # if current_user.id == user.user_id():
        #     self.redirect('/edit')

class UpdateProfile(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('/templates/update.html')
        self.response.write(template.render())
    def post(self):
        user = users.get_current_user()
        user_object = User.query(User.id == user.user_id()).get()
        user_object.name = self.request.get('name')
        user_object.type = self.request.get('type')
        user_object.grade = self.request.get('grade')
        user_object.zipcode = self.request.get('zipcode')

        user_object.put()

        title = []
        content = []
        user = users.get_current_user()
        profile_info = User.query(User.id == user.user_id()).get()
        user_name = profile_info.name
        user_posts = profile_info.posts
        for user_post in user_posts:
            title.append(user_post.get().title)
            content.append(user_post.get().content)

        if len(user_object.name) != 0:
            first_letter = user_object.name[0].upper()
        else:
            first_letter = ""

        template_vars = {
        'name': user_object.name,
        'first_letter': first_letter,
        'type': user_object.type,
        'zipcode': user_object.zipcode,
        'grade': user_object.grade,
        'length': len(title),
        'title': title,
        'content': content,
        'email': profile_info.email
        }

        template = env.get_template('/templates/profile.html')
        self.response.write(template.render(template_vars))
        # self.redirect('/profile')

class User(ndb.Model):
    name = ndb.StringProperty()
    type = ndb.StringProperty()
    zipcode = ndb.StringProperty()
    grade = ndb.StringProperty()
    id = ndb.StringProperty()
    posts = ndb.KeyProperty(kind = "Post", repeated= True)
    email = ndb.StringProperty()

class Post(ndb.Model):
    title = ndb.StringProperty()
    type = ndb.StringProperty()
    content = ndb.StringProperty()
    author = ndb.KeyProperty(kind = "User")
    author_name = ndb.StringProperty()

#testing method for posts
def addPost(title, type, content):
    matching_post = Post.query().filter(Post.title == title).filter(Post.type == type).filter(Post.content == content).fetch()
    # Only add if post does not exist in db.
    if len(matching_post) == 0:
        new_post = Post(title=title, type=type, content=content)
        new_post.put()


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/join', SignUp),
    ('/view_posts', ViewPosts),
    ('/create_profile', ProfileHandler),
    ('/post', CreatePost),
    ('/profile', ShowProfile),
    ('/edit', UpdateProfile),
], debug=True)
