from mainhandler import Handler
from models.blogmodel import Blog
from google.appengine.ext import db
# User of the post can not be able to like their post. only other user like


class LikePost(Handler):
    def get(self, post_id):
        if not self.user:
            self.redirect('/blog/login?error=You need to be logged')
        else:
            key = db.Key.from_path('Blog', int(post_id))
            post = db.get(key)
            user = post.user
            logged_user = self.user
            if logged_user in post.liked_by:
                error = "Already You liked this post"
                self.render("error.html", error=error)
            else:
                if user == logged_user:
                    error = "You can't like your own post"
                    self.render("error.html", error=error)
                else:
                    post.likes += 1
                    post.liked_by.append(logged_user)
                    post.put()
                    self.redirect("/blog")
