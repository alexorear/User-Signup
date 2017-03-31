#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re


#Standard page header
page_header = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>User Signup</title>
    </head>
    <body>"""

#Standard page footer
page_footer = """
    </body>
    </html>"""


class Index(webapp2.RequestHandler):
    def get(self):

        username = self.request.get('username')

        form_title = "<h2> User Signup </h2>"
        #User input form html
        username_label = "<label> Username </label>"
        username_input = "<input type='text' name='username'  value='{0}'/>" .format(username)

        password_label = "<label> Password </label>"
        password_input = "<input type='password' name='password'/>"

        ver_password_label = "<label> Verify Password </label>"
        ver_password_input = "<input type='password' name='ver_password'/>"

        email_label = "<label> Email (optional) </label>"
        email_input = "<input type='text' name='email'/>"

        submit = "<input type='submit'/>"

        # if we have an error display an error message
        username_error = self.request.get("username_error")
        pass_error = self.request.get("password_error")
        email_error = self.request.get("email_error")

        if username_error:
            error_esc = cgi.escape(username_error, quote=True)
            username_error = "<strong style='color:red'>" + error_esc + "</strong>"

        if pass_error:
            error_esc = cgi.escape(pass_error, quote=True)
            pass_error =  "<strong style='color:red'>" + error_esc + "</strong>"

        if email_error:
            error_esc = cgi.escape(email_error, quote=True)
            email_error =  "<strong style='color:red'>" + error_esc + "</strong>"



        # form concantination
        form = ("<form action='/Welcome' method='post'>" +
                username_label + username_input + username_error + '<br>' + '<br>' +
                password_label + password_input + pass_error + '<br>' + '<br>' +
                ver_password_label + ver_password_input + '<br>' + '<br>' +
                email_label + email_input + email_error + '<br>' + '<br>' + submit + '<br>'
                "</form>")


        content = page_header + form_title + form + page_footer
        self.response.write(content)

class Welcome(webapp2.RequestHandler):
    def post(self):
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

        if not valid_username(username):
            error = " Please enter a valid username"
            self.redirect("/?username_error=" + error)

        elif not valid_password(password):
            error =" Please enter a valid password"
            self.redirect("/?password_error=" + error)

        elif password != ver_password:
            error = " Passwords don't match"
            self.redirect("/?password_error=" + error)

        elif len(email) > 0:
            if not valid_email(email):
                error = " Please enter a valid email"
                self.redirect("/?email_error=" + error)


        content = page_header + '<p> Welecome ' + username + '</p>' + page_footer
        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/Welcome', Welcome)
], debug=True)
