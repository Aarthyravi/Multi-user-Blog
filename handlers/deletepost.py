from mainhandler import Handler
from models.blogmodel import Blog
from google.appengine.ext import db
# User of the post can only be able to delete their post


class DeletePost(Handler):
    def get(self, post_id):
        if not self.user:
            self.redirect('/blog/login?error=You need to be logged')
        else:
            key = db.Key.from_path('Blog', int(post_id))
            post = db.get(key)
            if not post:
                self.error(404)
                return
            if not self.user:
                self.redirect('/blog/login')
            user = post.user
            loggedUser = self.user
            if user == loggedUser:
                key = db.Key.from_path('Blog', int(post_id))
                post = db.get(key)
                post.delete()
                self.render("deletepost.html")
            else:
                error = "You can't delete this post"
                self.render("error.html", error=error)
