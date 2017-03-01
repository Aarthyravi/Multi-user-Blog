from handlers.mainhandler import Handler
from models.blogmodel import Blog
from google.appengine.ext import db
import userstuff
# Single post display with comments


class BlogPost(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Blog', int(post_id))
        post = db.get(key)
        if not post:
            self.error(404)
            return self.redirect('nopost.html')
        self.render("post1.html", post=post)
