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
import logging
import string
from datetime import datetime
import webapp2
import os

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import mail

from StudentsAdmin import StudentsAdmin
from Exceptions import *

BGU_MAIL_SUFFIX = "@post.bgu.ac.il"

def showMessage(handler, message):
    path = os.path.join(os.path.dirname(__file__), 'message.htm')
    template_values = {
            'message': message,
        }
    handler.response.out.write(template.render(path, template_values))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        pass

class CheckExamsHandler(webapp2.RequestHandler):
    def get(self):
        stdAdmin = StudentsAdmin(self.request.application_url)
        self.response.out.write(stdAdmin.checkExams())

class UnregisterHandler(webapp2.RequestHandler):
    def post(self):
        username = self.request.get('username')
        id_num = self.request.get('id_num')
        email = self.request.get('username') + BGU_MAIL_SUFFIX
        gql =   "SELECT * " \
                "FROM Student " \
                "WHERE username = '%s' " \
                "AND id_num = '%s' " \
                "AND email = '%s'" % (username, id_num, email)
        logging.info(gql)
        students =  db.GqlQuery(gql)
        user_removed = False
        for student in students:
            student.delete()
            showMessage(self, "ההרשמה בוטלה")
            user_removed = True
            logging.info("user %s unregistered" % username)
        if not user_removed:
            showMessage(self, "המשתמש לא נמצא")
            logging.info("Could not find user %s" % username)

class RegisterHandler(webapp2.RequestHandler):
    def post(self):
        stdAdmin = StudentsAdmin(self.request.application_url)
        try:
            stdAdmin.register(
                    self.request.get("user"),
                    self.request.get("password"),
                    self.request.get("id_num"),
                    self.request.get("user") + BGU_MAIL_SUFFIX,
                    #self.request.get("email"),
                    )
        except LoginException as e:
            showMessage(self, e.message)
            return

        showMessage(self, "ההרשמה הצליחה!")

class ApprovalHandler(webapp2.RequestHandler):
    def get(self):
        email = self.request.get("email")
        approval_code = self.request.get("code")
        students =  db.GqlQuery("SELECT * "
                                "FROM Student "
                                "WHERE email = '%s'" % email)
        found = False
        for student in students:
            if student.email_approval_code == approval_code:
                student.email_approved = True
                student.put()
                self.response.out.write("Ok, all done.<br>"
                    "You will be notified about changes in your exams.")
                logging.info("address %s confirmed" % email)
                found = True
            else:
                self.response.out.write("Wrong confirmation code.")
        if not found:
            self.response.out.write("Could not find %s" % email)

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/checkExams', CheckExamsHandler),
                               ('/unregister', UnregisterHandler),
                               ('/register', RegisterHandler),
                               ('/approve', ApprovalHandler),
                               ],
                              debug=True)
