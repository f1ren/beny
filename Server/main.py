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
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import blobstore_handlers
import os
import webapp2
import StringIO

from PhysWeb import PhysWeb

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')

class UploadHandler(webapp2.RequestHandler):
    def post(self):
        try:
            physWeb = PhysWeb()
            uname = self.request.get('uname')
            password = self.request.get('password')
            path = self.request.get('path')
            exnum = self.request.get('exnum')
            exercise = StringIO.StringIO(self.request.get('exercise'))
            physWeb.submitExercise(uname, password, path, exnum, exercise)
            self.response.out.write("ok")
        except AssertionError, e:
            self.response.out.write(e.args)

app = webapp2.WSGIApplication([
                              ('/', MainHandler),
                              ('/upload', UploadHandler),
                              ],
                              debug=True)
