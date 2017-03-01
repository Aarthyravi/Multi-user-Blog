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


def valid_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return username and USER_RE.match(username)


def valid_password(password):
    PASS_RE = re.compile(r"^.{3,20}$")
    return password and PASS_RE.match(password)


def valid_email(email):
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return not email or EMAIL_RE.match(email)
