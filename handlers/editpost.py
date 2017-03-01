from handlers.mainhandler import Handler
from models.blogmodel import Blog
from google.appengine.ext import db
# User of the post can only be able to edit their post


class EditPost(Handler):
    def get(self, post_id):
        """ get the post of the post_id for editing"""
        if not self.user:
            self.redirect('/blog/login?error=You need to be logged')
            return
        else:
            key = db.Key.from_path('Blog', int(post_id))
            post = db.get(key)
            if not post:
                self.error(404)
                return
            user = post.user
            loggedUser = self.user
            if user == loggedUser:
                key = db.Key.from_path('Blog', int(post_id))
                post = db.get(key)
                error = ""
                self.render("editpost.html", subject=post.subject,
                            content=post.content, post_id=post_id,
                            error=error)
            else:
                error = "You can't edit this post"
                self.render("error.html", error=error)

    def post(self, post_id):
        if not self.user:
            self.redirect("/blog/login")
            return
        else:
            key = db.Key.from_path('Blog', int(post_id))
            post = db.get(key)
            if not post:
                self.error(404)
                return
            user = post.user
            loggedUser = self.user
            if user == loggedUser:
                subject = self.request.get('subject')
                content = self.request.get('content')
                if subject and content:
                    post.subject = subject
                    post.content = content
                    post.put()
                    self.redirect('/blog/%s' % str(post.key().id()))
                else:
                    error = "subject and content, please!"
                    self.render("editpost.html", subject=subject,
                                content=content, post_id=post_id,
                                error=error)
            else:
                error = "You can't edit this post"
                self.render("error.html", error=error)
