from handlers.mainhandler import Handler
import userstuff
# Once the logging page / Signup page
# is valid then the welcome page is displayed
# wuth username and logout


class WelcomeHandler(Handler):
    def get(self):
        user = self.request.cookies.get('user')
        if user:
            username = userstuff.check_secure(user)
            if username:
                self.render('welcome.html', username=username)
            else:
                self.redirect('/blog/signup')
                return
        else:
            self.redirect('/blog/signup')
            return
