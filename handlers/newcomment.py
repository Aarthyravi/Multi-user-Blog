from mainhandler import Handler
from models.blogmodel import Blog
from models.commentmodel import Comment
from google.appengine.ext import db
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
