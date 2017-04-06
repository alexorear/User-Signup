import webapp2
import cgi
import re
import jinja2
import os

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    autoescape=True)

class Index(webapp2.RequestHandler):
    def get(self):

        template = env.get_template('signup.html')
        content = template.render()
        self.response.write(content)

    def post(self):
        # escape and define variables from user input form
        username = self.request.get("username")
        password = self.request.get("password")
        ver_password = self.request.get("ver_password")
        email = self.request.get("email")

        # check for regular expressions to validate username, password and email
        user_reg = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        def valid_username(username):
            return user_reg.match(username)

        password_reg = re.compile(r"^.{3,20}$")
        def valid_password(password):
            return password_reg.match(password)

        email_reg = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        def valid_email(email):
            return email_reg.match(email)

        # Check for validation errors
        valid_error = False
        username_error = ""
        pass_error = ""
        email_error = ""

        if not valid_username(username):
            username_error = "Please enter a valid username"
            valid_error = True

        if not valid_password(password):
            pass_error = "Please enter a valid password"
            valid_error = True

        if password != ver_password:
            pass_error = "Passwords don't match"
            valid_error = True

        if len(email) > 0:
            if not valid_email(email):
                email_error = "Please enter a valid email"
                valid_error = True

        if valid_error == True:
            """if we have an error display an error message"""
            template = env.get_template('signup.html')
            content = template.render(username_error = username_error,
                username = username, pass_error = pass_error,
                email_error = email_error, email = email)

            self.response.write(content)

        else:
            self.redirect("/Welcome?username=" + username)


class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")

        template = env.get_template('welcome.html')
        content = template.render(username = username)
        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/Welcome', Welcome)
], debug=True)
