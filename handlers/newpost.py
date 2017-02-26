from handlers.mainhandler import Handler
from models.blogmodel import Blog
from userstuff import *
# Valid user have to post the new post with subject and content
class NewPost(Handler):
     def get(self):
         if self.user:
             self.render("newpost.html")
         else:
             self.redirect("/blog/login")

     def post(self):
         if not self.user:
            self.redirect('/blog/login')
         subject = self.request.get('subject')
         content = self.request.get('content')
         user = self.read_secure_cookie('user')

         if subject and content :
             b = Blog(subject = subject,content= content,user=user,likes=0)
             post_id = b.put().id()
             self.redirect('/blog/%s' %post_id)
         else:
             error = "We need both a Subject and some content"
             self.render("newpost.html",subject=subject,content=content,error=error)
