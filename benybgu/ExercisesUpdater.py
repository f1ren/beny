#!/usr/bin/env python

from google.appengine.ext import db
import urllib2
import logging

from Exercises import Exercises
from dbModels import *

class ExercisesUpdater(object):
    def update(self):
        exercisesParser = Exercises()
        courses = db.GqlQuery("SELECT * FROM Course")
        for course in courses:
            try:
                logging.info("Getting exercise of %s" % course.name)
                exercises =\
                    exercisesParser.getAllExercisesFromUrl(course.submitURL)
                logging.info("Parsing %s" % course.name)
                for ex in exercises:
                    if ex is None: continue
                    dbEx = Exercise(key_name=ex[3])
                    dbEx.course = course.name
                    (dbEx.number, dbEx.published, dbEx.topic, dbEx.exerciseUrl,\
                     dbEx.solutionUrl, dbEx.deadline, dbEx.uploadUrl) = \
                     map(lambda x: x.replace('\n',''), ex)
                    dbEx.put()
            except urllib2.HTTPError:
                logging.info("404 error")
            except ValueError:
                logging.info("invalid url")
