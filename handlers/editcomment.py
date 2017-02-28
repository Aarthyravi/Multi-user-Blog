from mainhandler import Handler
from models.commentmodel import Comment
from google.appengine.ext import db
from handlers.error import CommentError
# user of the comment can only be able to edit their comment.
class EditComment(Handler):
    def get(self, post_id,comment_id):
        if not self.user:
            self.redirect("/blog/login")
            return
        key = db.Key.from_path('Comment', int(comment_id))
        c = db.get(key)
        if c.author == self.user:
          comment = Comment.get_by_id(int(comment_id))
          if comment:
             self.render("editcomment.html",comment=comment.comment)
          else:
            self.redirect('/commenterror')
        else:
            error = "You can't edit this comment"
            self.render("error.html",error=error)

    def post(self, post_id, comment_id):
            comment = Comment.get_by_id(int(comment_id))
            comment.comment = self.request.get('comment')
            comment.put()
            self.redirect('/blog/%s' % str(post_id))
