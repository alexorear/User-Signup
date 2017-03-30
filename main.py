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

        form_title = "<h2> User Signup </h2>"
        #User input form html
        username_label = "<label> Username </label>"
        username_input ="<input type='text' name='username'/>"

        password_label = "<label> Password </label>"
        password_input = "<input type='password' name='password'/>"

        ver_password_label = "<label> Verify Password </label>"
        ver_password_input = "<input type='password' name='ver_password'/>"

        email_label = "<label> Email (optional) </label>"
        email_input = "<input type='text' name='email'/>"

        submit = "<input type='submit'/>"

        # if we have an error display an error message
        username_error = self.request.get("username_error")
        pass_error = self.request.get("pass_error")

        if username_error:
            error_esc = cgi.escape(username_error, quote=True)
            username_error = "<strong style='color:red'>" + error_esc + "</strong>"
        if pass_error:
            error_esc = cgi.escape(pass_error, quote=True)
            pass_error =  "<strong style='color:red'>" + error_esc + "</strong>"

        # form concantination
        form = ("<form method='post'>" +
                username_label + username_input + username_error + '<br>' + '<br>' +
                password_label + password_input + pass_error + '<br>' + '<br>' +
                ver_password_label + ver_password_input + '<br>' + '<br>' +
                email_label + email_input + '<br>' + '<br>' + submit + '<br>'
                "</form>")


        content = page_header + form_title + form + page_footer
        self.response.write(content)

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        ver_password = self.request.get("ver_password")
        email = self.request.get("email")

        if len(username) < 1:
            error = " Please enter a valid username"
            self.redirect("/?username_error=" + error)

        if password != ver_password:
            error = " Passwords don't match"
            self.redirect("/?pass_error=" + error)



        self.response.write("New user has been added.")

class Welcome(webapp2.RequestHandler):
    def get(self):
        self.responce.write("Thanks, NEW USER NAME, has been successfully added!")


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/Welcome', Welcome)
], debug=True)
