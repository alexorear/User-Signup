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

def build_page():
    #Standard page header
    page_header = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>User Signup</title>
        </head>
        <body>
            <h2>User Signup</h2>"""

    #Standard page footer
    page_footer = """
        </body>
        </html>"""

    #Page content
    username_label = "<label> Username </label>"
    username_input ="<input type='text' name='username'/>"

    password_label = "<label> Password </label>"
    password_input = "<input type='password' name='password'/>"

    ver_password_label = "<label> Verify Password </label>"
    ver_password_input = "<input type='password' name='ver_password'/>"

    email_label = "<label> Email (optional) </label>"
    email_input = "<input type='text' name='email'/>"

    submit = "<input type='submit'/>"

    form = ("<form method='post'>" +
            username_label + username_input + '<br>' + '<br>' +
            password_label + password_input + '<br>' + '<br>' +
            ver_password_label + ver_password_input + '<br>' + '<br>' +
            email_label + email_input + '<br>' + '<br>' + submit + 
            "</form>")

    return page_header + form + page_footer



class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(build_page())

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
