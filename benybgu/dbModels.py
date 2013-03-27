#!/usr/bin/env python

from google.appengine.ext import db

class Course(db.Model):
  name = db.StringProperty()
  submitURL = db.StringProperty()

class Exercise(db.Model):
    course = db.StringProperty()
    number = db.StringProperty()
    published = db.StringProperty()
    topic = db.StringProperty(multiline=True)
    exerciseUrl = db.StringProperty()
    solutionUrl = db.StringProperty()
    deadline = db.StringProperty()
    uploadUrl = db.StringProperty()
