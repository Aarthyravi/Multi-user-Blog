import os
import re
import hashlib
import hmac
import random
import string
import webapp2
import jinja2

# set The Secret code. No one track the cookies value.
SECRET = 'imsosecret'
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)

# User Security
def make_secure(s):
    return "%s|%s" %(s,hmac.new(SECRET,s).hexdigest())

def check_secure(h):
    val = h.split('|')[0]
    if h == make_secure(val):
      return val

def make_salt():
    return ''.join(random.choice(string.letters) for i in range(5))

def make_pw_hash(name,password,salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + password + salt).hexdigest()
    return '%s|%s' %(h,salt)

def valid_pw(name,password,h):
    salt = h.split('|')[1]
    return h == make_pw_hash(name,password,salt)

def users_key(group='default'):
    return db.Key.from_path('users', group)

# templates
class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.write(*a,**kw)

    def render_str(self,template,**param):
        param['user'] = self.user
        t = jinja_env.get_template(template)
        return t.render(param)

    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure(cookie_val)

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        self.user = self.read_secure_cookie('user')

#User Model
class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty(required = False)

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls,name):
        u = User.all().filter('name =',name).get()
        return u

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u

# Login Handler with username & Password
class LoginHandler(Handler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username,password)
        if u:
            new_cookie = make_secure(str(username))
            self.response.headers.add_header('Set-Cookie', 'user=%s; Path=/' % new_cookie)
            self.redirect('/blog/welcome')
        else:
            msg = 'Invalid login'
            self.render('login.html', error = msg)

# Logout Handler
class LogoutHandler(Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'user=; Path=/')
        self.redirect('/blog/signup')

# Signup Handler with username,password,Verify password and optional email and check the Validation for all field.
class SignupHandler(Handler):
    def get(self):
        self.render("signup.html")

    def post(self):
        error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        param = dict(username = username,password = password,email=email)
        if not valid_username(username):
             param['error_username']="This is not a valid username"
             error = True
        if not valid_password(password):
            param['error_password']="This is not a valid password"
            error = True
        elif password != verify:
            param['error_verify']="Your password didn't match"
            error = True
        if not valid_email(email):
            param['error_email']="This is not a valid email"
            error = True
        if error:
            self.render("signup.html",**param)
        else:
            u = User.by_name(username)
            if u:
                msg = 'This username already exists!'
                self.render('signup.html', error_username = msg)
            else:
                u = User(name=username, pw_hash=make_pw_hash(username, password), email=email)
                u.put()
                new_cookie = make_secure(str(username))
                self.response.headers.add_header('Set-Cookie', 'user=%s; Path=/' % new_cookie)
                self.redirect('/blog/welcome')

# Once the logging page / Signup page is valid then the welcome page is displayed wuth username and logout
class WelcomeHandler(Handler):
       def get(self):
           user = self.request.cookies.get('user')
           if user:
               username = check_secure(user)
               if username:
                  self.render('welcome.html', username=username)
               else:
                  self.redirect('/blog/signup')
           else:
               self.redirect('/blog/signup')

# validation function for username,password & email
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

# Blog Model
class Blog(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    lastmodi = db.DateTimeProperty(auto_now = True)
    user = db.StringProperty(required = True)
    likes = db.IntegerProperty(required=True)
    liked_by = db.ListProperty(str)

    @property
    def comments(self):
        return Comment.all().filter("post = ", str(self.key().id()))

# Front page of Blog
class MainPage(Handler):
    def get(self):
      blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC limit 10")
      self.render("front.html",blogs=blogs)

# Valid user have to post the new post with subject and content
class NewPost(Handler):
     def get(self):
         if self.user:
            self.render("newpost.html")
         else:
           self.redirect("/blog/login")

     def post(self):
         if not self.user:
            self.redirect('/blog/login')
         subject = self.request.get('subject')
         content = self.request.get('content')
         user = self.read_secure_cookie('user')

         if subject and content :
             b = Blog(subject = subject,content= content,user=user,likes=0)
             post_id = b.put().id()
             self.redirect('/blog/%s' %post_id)
         else:
             error = "We need both a Subject and some content"
             self.render("newpost.html",subject=subject,content=content,error=error)

# User of the post can only be able to edit their post
class EditPost(Handler):
    def get(self, post_id):
        if not self.user:
            self.redirect('/blog//login')
        else:
            key = db.Key.from_path('Blog', int(post_id))
            post = db.get(key)
            user = post.user
            loggedUser = self.user

            if user == loggedUser:
                key = db.Key.from_path('Blog', int(post_id))
                post = db.get(key)
                error = ""
                self.render("editpost.html", subject=post.subject,
                            content=post.content, error=error)
            else:
                error = "You can't edit this post"
                self.redirect("error.html",error=error)

    def post(self, post_id):
        if not self.user:
            self.redirect("/login")
        else:
            key = db.Key.from_path('Blog', int(post_id))
            post = db.get(key)
            post.subject = self.request.get('subject')
            post.content = self.request.get('content')
            post.put()
            self.redirect('/blog/%s' % str(post.key().id()))

# User of the post can not be able to like their post. only other user like
class LikePost(Handler):
    def get(self, post_id):
        if not self.user:
            self.redirect('/blog/login')
        else:
            key = db.Key.from_path('Blog', int(post_id))
            post = db.get(key)
            user = post.user
            logged_user = self.user

            if user == logged_user or logged_user in post.liked_by:
                error = "Already You liked this post"
                self.render("error.html",error=error)
            else:
                post.likes += 1
                post.liked_by.append(logged_user)
                post.put()
                self.redirect("/blog")

# User of the post can only be able to delete their post
class DeletePost(Handler):
    def get(self, post_id):
        if not self.user:
            self.redirect('/blog/login')
        else:
            key = db.Key.from_path('Blog', int(post_id))
            post = db.get(key)
            user = post.user
            loggedUser = self.user

            if user == loggedUser:
                key = db.Key.from_path('Blog', int(post_id))
                post = db.get(key)
                post.delete()
                self.render("deletepost.html")
            else:
                self.redirect("/blog")

# Single post display with comments
class BlogPost(Handler):
     def get(self,post_id):

         key = db.Key.from_path('Blog',int(post_id))
         post = db.get(key)

         if not post:
            self.error(404)
            return

         self.render("post.html",post=post)

# Comment Model
class Comment(db.Model):
    comment = db.StringProperty(required=True)
    post = db.StringProperty(required=True)
    author = db.StringProperty(required=True)

# Newcomment
class NewComment(Handler):
    def get(self, post_id):
        if not self.user:
            self.redirect("/blog/login")
            return

        self.render("newcomment.html")

    def post(self, post_id):
        key = db.Key.from_path('Blog', int(post_id))
        post = db.get(key)
        if not post:
            self.error(404)
            return

        if not self.user:
            self.redirect('/blog/login')

        comment = self.request.get('comment')

        if comment:
            author = self.request.get('author')
            c = Comment(comment=comment,post=post_id,author=author)
            c.put()
            self.redirect('/blog/%s' %post_id)
        else:
            error = "comment,Please!"
            self.render("newcomment.html", post=post, error=error)

# user of the comment can only be able to edit their comment.
class EditComment(Handler):
    def get(self, post_id,comment_id):
        comment = Comment.get_by_id(int(comment_id))
        if comment:
            self.render("editcomment.html",comment=comment.comment)
        else:
            self.redirect('/commenterror')

    def post(self, post_id, comment_id):
            comment = Comment.get_by_id(int(comment_id))
            comment.comment = self.request.get('comment')
            comment.put()
            self.redirect('/blog/%s' % str(post_id))

# user of the comment can only be able to delete their comment.
class DeleteComment(Handler):
    def get(self, post_id, comment_id):
        comment = Comment.get_by_id(int(comment_id))
        if comment:
            comment.delete()
            self.redirect('/blog/%s' % str(post_id))
        else:
            self.redirect('/commenterror')

class CommentError(Handler):
    def get(self):
        self.write('Error')


app = webapp2.WSGIApplication([('/blog',MainPage),('/blog/signup',SignupHandler),
                             ('/blog/welcome',WelcomeHandler),
                             ('/blog/login',LoginHandler),
                             ('/blog/logout',LogoutHandler),('/blog/newpost',NewPost),
                             ('/blog/(\d+)/deletepost',DeletePost),
                             ('/blog/(\d+)/editpost', EditPost),
                             ('/blog/(\d+)',BlogPost),
                             ('/blog/(\d+)/newcomment',NewComment),
                             ('/blog/(\d+)/likepost', LikePost),
                             ('/blog/(\d+)/editcomment/(\d+)',EditComment),
                             ('/blog/(\d+)/deletecomment/(\d+)',DeleteComment),
                             ('/blog/commenterror',CommentError),],debug = True)
