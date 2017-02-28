from models.usermodel import User
from mainhandler import Handler
import mainhandler
# Signup Handler with username,password,Verify password and optional email and check the Validation for all field.
class SignupHandler(Handler):
    def get(self):
        self.render("signup.html")

    def post(self):
        error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        param = dict(username = username,password = password,email=email)
        if not valid_username(username):
             param['error_username']="This is not a valid username"
             error = True
        if not valid_password(password):
            param['error_password']="This is not a valid password"
            error = True
        elif password != verify:
            param['error_verify']="Your password didn't match"
            error = True
        if not valid_email(email):
            param['error_email']="This is not a valid email"
            error = True
        if error:
            self.render("signup.html",**param)
        else:
            u = User.by_name(username)
            if u:
                msg = 'This username already exists!'
                self.render('signup.html', error_username = msg)
            else:
                u = User(name=username, pw_hash=make_pw_hash(username, password), email=email)
                u.put()
                new_cookie = make_secure(str(username))
                self.response.headers.add_header('Set-Cookie', 'user=%s; Path=/' % new_cookie)
                self.redirect('/blog/welcome')
