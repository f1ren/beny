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
from google.appengine.ext import db
import os
import webapp2
import StringIO

from PhysWeb import PhysWeb

import cgi
import urllib
from Courses import Courses


class Course(db.Model):
  name = db.StringProperty()
  submitURL = db.StringProperty()

def addCourse(name, url):
    course_key = db.Key.from_path('Course', name) 
    course = db.get(course_key)
    if course is None:
      course = Course(key_name=name)
    course.name = name
    course.submitURL = url
    course.put()
	
def removeCourse(name):
	course_key = db.Key.from_path('Course', name)
	db.delete(course_key)
    
def update():
    c = Courses()
    courseList = c.getAllCourses()
    for course in courseList:
      addCourse(course[0],course[1])

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')

    self.response.out.write("""
          <form action="/add" method="post">
            <div><textarea name="name" rows="1" cols="30"></textarea></div>
			<div><textarea name="url" rows="1" cols="30"></textarea></div>
			<div><input type="submit" value="Add course"></div>
          </form><br>
		  <form action="/remove" method="post">
            <div><textarea name="name" rows="1" cols="30"></textarea></div>
			<div><input type="submit" value="Remove course"><input type="submit" value="Remove all courses"></div>
          </form>

          <form action="/update" method="post">
			<div><input type="submit" value="Update list"></div>
          </form>
        </body>
      </html>""")
	
    courses = db.GqlQuery("SELECT * "
                            "FROM Course ")

    for course in courses:
      self.response.out.write('Course Name: <b>%s</b> URL: <b>%s</b><br>'
	                           % (course.name, cgi.escape(course.submitURL)))


class AddCourse(webapp2.RequestHandler):
  def post(self):
    course_name = self.request.get('name')
    course_URL = self.request.get('url')
    addCourse(course_name, course_URL)
    self.redirect('/')

	
class RemoveCourse(webapp2.RequestHandler):
  def post(self):
    course_name = self.request.get('name')
    removeCourse(course_name)
    self.redirect('/')

    
class RemoveAllCourses(webapp2.RequestHandler):
  def post(self):
    courses = db.GqlQuery("SELECT * "
                          "FROM Course ")
    for course in courses:
      removeCourse(course.name)
    self.redirect('/')
    
    
class Update(webapp2.RequestHandler):
  def post(self):
    update()
    self.redirect('/')
    

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

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/add', AddCourse),
							   ('/remove', RemoveCourse),
                               ('/removeAll', RemoveAllCourses),
                               ('/update', Update)],
                               ('/upload', UploadHandler),
                               ],
                               debug=True)
