from google.appengine.ext import db
from models.commentmodel import Comment
# Blog Model


class Blog(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    lastmodi = db.DateTimeProperty(auto_now=True)
    user = db.StringProperty(required=True)
    likes = db.IntegerProperty(required=True)
    liked_by = db.ListProperty(str)

    @property
    def comments(self):
        return Comment.all().filter("post = ", str(self.key().id()))
