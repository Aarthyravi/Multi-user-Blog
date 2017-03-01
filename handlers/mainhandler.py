import userstuff
import webapp2
from models.usermodel import User


class Handler(webapp2.RequestHandler):
    """ class name : Handler
        render the pages with jinja templates """
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **param):
        param['user'] = self.user
        t = userstuff.jinja_env.get_template(template)
        return t.render(param)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and userstuff.check_secure(cookie_val)

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        self.user = self.read_secure_cookie('user')
