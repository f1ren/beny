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
from google.appengine.ext import db
import os
import webapp2
import StringIO
import json
import logging

from PhysWeb import PhysWeb
from dbModels import *
from ExercisesUpdater import ExercisesUpdater
import utils

import cgi
from Courses import Courses

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
    
def updateCourses():
    logging.info("Updating courses")
    c = Courses()
    courseList = c.getAllCourses()
    for course in courseList:
      addCourse(course[0],course[1])

class MainPage(webapp2.RequestHandler):
  def get(self):

    self.response.out.write("""
      <html>
        <body>
          <form action="/add" method="post">
            <div>
              Course Name <textarea name="name" rows="1" cols="30"></textarea><br>
			  Course URL  <textarea name="url" rows="1" cols="30"></textarea><br>
			  <input type="submit" value="Add course">
            </div>
          </form>
		  <form action="/remove" method="post">
            <div>
              Course Name <textarea name="name" rows="1" cols="30"></textarea><br>
			  <input type="submit" value="Remove course">
            </div>
          </form>
          <form action="/removeAll" method="post">
            <div><input type="submit" value="Remove all courses"></div>
          </form>
          <form action="/update" method="post">
			<div><input type="submit" value="Update list"></div>
          </form>
          <a href="/json">JSON output</a><br><br>
          <form action="/removeSelected" method="post">
            <div><input type="submit" value="Remove selected courses"></div>
          </form>""")
	
    self.response.out.write("""
          <div><table border="1"> 
            <tr><th/><th>Course Name</th><th>Submission URL</th></tr>
            """)
    courses = db.GqlQuery("SELECT * FROM Course")
    for course in courses:
      self.response.out.write("""
            <tr>
              <td><input type="checkbox" name="course" value="%s"></td>
              <td>%s</td><td>%s</td>
            </tr>
            """ % (course.name, course.name, cgi.escape(course.submitURL)))
    self.response.out.write("""
          </div></table>
        </body>
      </html>""")
                               
class JSON(webapp2.RequestHandler):
  def get(self):
    result = dict()
    courses = db.GqlQuery("SELECT * FROM Course")
    for course in courses:
      result[course.name] = course.submitURL
    self.response.out.write(json.dumps(result, sort_keys=True))
    
class ExercisesOfCourse(webapp2.RequestHandler):
  def get(self):
    result = []
    course_name = self.request.get('course')
    exercises = db.GqlQuery("SELECT * FROM Exercise WHERE course = :1", \
            course_name)
    for exercise in exercises:
        result.append(utils.to_dict(exercise))
    self.response.out.write(json.dumps(result, sort_keys=True))

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
    

class RemoveSelected(webapp2.RequestHandler):
  def post(self):
    self.redirect('/')
    
    
class UpdateCourses(webapp2.RequestHandler):
  def get(self):
    updateCourses()
    
class UpdateExercises(webapp2.RequestHandler):
    def get(self):
        eu = ExercisesUpdater()
        eu.update()

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
                               ('/json', JSON),
                               ('/courses', JSON),
                               ('/exercises', ExercisesOfCourse),
                               ('/add', AddCourse),
							   ('/remove', RemoveCourse),
                               ('/removeAll', RemoveAllCourses),
                               ('/removeSelected', RemoveSelected),
                               ('/updateCourses', UpdateCourses),
                               ('/updateExercises', UpdateExercises),
                               ('/upload', UploadHandler)],
                               debug=True)
