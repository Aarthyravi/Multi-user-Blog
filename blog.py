from google.appengine.ext import db
import webapp2
# Models
from models.blogmodel import Blog
from models.commentmodel import Comment
from models.usermodel import User

# Handlers
from mainhandler import Handler
from handlers.deletecomment import DeleteComment
from handlers.deletepost import DeletePost
from handlers.editcomment import EditComment
from handlers.editpost import EditPost
from handlers.error import CommentError
from handlers.frontblog import MainPage
from handlers.likepost import LikePost
from handlers.login import LoginHandler
from handlers.logout import LogoutHandler
from handlers.newcomment import NewComment
from handlers.newpost import NewPost
from handlers.post import BlogPost
from handlers.signup import SignupHandler
from handlers.welcome import WelcomeHandler

app = webapp2.WSGIApplication([('/blog',MainPage),('/',MainPage),('',MainPage),
                             ('/blog/signup',SignupHandler),
                             ('/blog/welcome',WelcomeHandler),
                             ('/blog/login',LoginHandler),
                             ('/blog/logout',LogoutHandler),('/blog/newpost',NewPost),
                             ('/blog/(\d+)/deletepost',DeletePost),
                             ('/blog/(\d+)/editpost', EditPost),
                             ('/blog/(\d+)',BlogPost),
                             ('/blog/(\d+)/newcomment',NewComment),
                             ('/blog/(\d+)/likepost', LikePost),
                             ('/blog/(\d+)/editcomment/(\d+)',EditComment),
                             ('/blog/(\d+)/deletecomment/(\d+)',DeleteComment),
                             ('/blog/commenterror',CommentError),],debug = True)
