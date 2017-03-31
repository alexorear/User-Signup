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
        email = self.request.get('email')

        form_title = "<h2> User Signup </h2>"
        #User input form html
        username_label = "<label> Username </label>"
        username_input = "<input type='text' name='username'  value='{0}'/>" .format(username)

        password_label = "<label> Password </label>"
        password_input = "<input type='password' name='password'/>"

        ver_password_label = "<label> Verify Password </label>"
        ver_password_input = "<input type='password' name='ver_password'/>"

        email_label = "<label> Email (optional) </label>"
        email_input = "<input type='text' name='email' value='{0}'/>" .format(email)

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
        # escape and define variables from user input form
        username = cgi.escape(self.request.get("username"), quote=True)
        password = cgi.escape(self.request.get("password"),quote=True)
        ver_password = cgi.escape(self.request.get("ver_password"),quote=True)
        email = cgi.escape(self.request.get("email"),quote=True)

        valid_error = False
        url_param = []

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
        if not valid_username(username):
            user_error = "username_error=Please enter a valid username &username=" + username
            #self.redirect("/?username_error=" + error + "&username=" + username)
            url_param.append(user_error)
            valid_error = True
        else:
            url_param.append("username=" + username)

        if not valid_password(password):
            pass_error ="password_error=Please enter a valid password"
            #self.redirect("/?password_error=" + error)
            url_param.append(pass_error)
            valid_error = True

        if password != ver_password:
            pass_error = "password_error=Passwords don't match"
            #self.redirect("/?password_error=" + error)
            url_param.append(pass_error)
            valid_error = True

        if len(email) > 0:
            if not valid_email(email):
                email_error = "email_error=Please enter a valid email &email=" + email
                #self.redirect("/?email_error=" + error + "&email=" + email)
                url_param.append(email_error)
                valid_error = True

        if valid_error == True:
            redirect_message = ""
            for i in url_param:
                redirect_message += (i + "&")
            self.redirect("/?" + redirect_message )

        content = page_header + '<h2>Welcome ' + username + '!</h2>' + page_footer
        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/Welcome', Welcome)
], debug=True)
