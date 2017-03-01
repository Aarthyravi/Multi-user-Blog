from models.usermodel import User
from handlers.mainhandler import Handler
import userstuff
# Login Handler with username & Password


class LoginHandler(Handler):
    def get(self):
        self.render('login.html', error=self.request.get('error'))

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            new_cookie = userstuff.make_secure(str(username))
            self.response.headers.add_header('Set-Cookie',
                                             'user=%s; Path=/' % new_cookie)
            self.redirect('/blog/welcome')
        else:
            msg = 'Invalid login'
            self.render('login.html', error=msg)
