from mainhandler import Handler
# Logout Handler


class LogoutHandler(Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'user=; Path=/')
        self.redirect('/blog/signup')
