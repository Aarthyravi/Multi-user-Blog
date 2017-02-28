import os
import re
import hashlib
import hmac
import random
import string
import webapp2
import jinja2
from google.appengine.ext import db

# set The Secret code. No one track the cookies value.
SECRET = 'imsosecret'

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

# User Security


def make_secure(s):
    """ Make Hash with hmac"""
    return "%s|%s" % (s, hmac.new(SECRET, s).hexdigest())


def check_secure(h):
    """ Check security"""
    val = h.split('|')[0]
    if h == make_secure(val):
        return val


def make_salt():
    """ Make Salt """
    return ''.join(random.choice(string.letters) for i in range(5))


def make_pw_hash(name, password, salt=None):
    """ Make Password Hash"""
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + password + salt).hexdigest()
    return '%s|%s' % (h, salt)


def valid_pw(name, password, h):
    """ Check valid password """
    salt = h.split('|')[1]
    return h == make_pw_hash(name, password, salt)

# Model Keys


def users_key(group='default'):
    return db.Key.from_path('users', group)

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


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **param):
        param['user'] = self.user
        t = jinja_env.get_template(template)
        return t.render(param)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure(cookie_val)

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        self.user = self.read_secure_cookie('user')
