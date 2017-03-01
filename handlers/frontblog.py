from handlers.mainhandler import Handler
from models.blogmodel import Blog
from google.appengine.ext import db
# Front page of Blog


class MainPage(Handler):
    def get(self):
        blogs = db.GqlQuery("""SELECT * FROM Blog ORDER BY
                             created DESC limit 10""")
        self.render("front.html", blogs=blogs)
