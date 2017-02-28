from mainhandler import Handler
import mainhandler
# Once the logging page / Signup page is valid then the welcome page is displayed wuth username and logout
class WelcomeHandler(Handler):
       def get(self):
           user = self.request.cookies.get('user')
           if user:
               username = check_secure(user)
               if username:
                  self.render('welcome.html', username=username)
               else:
                  self.redirect('/blog/signup')
           else:
               self.redirect('/blog/signup')
