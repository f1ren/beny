#!/usr/bin/env python

from google.appengine.api import urlfetch
from bs4 import BeautifulSoup
import urllib2
import logging
from logging import debug
from logging import info
import re

COURSES_LIST_URL = "http://physweb.bgu.ac.il/COURSES/"
COURSE_URL = "http://physweb.bgu.ac.il/COURSES/ProtoCourse/index.php?folder=%s#Home"

class Courses(object):
    def __init__(self):
        pass

    def _getMainCoursesList(self, bs):
        result = []
        for a in bs.findAll("a"):
            folder = a.getText()
            if folder[-1] == "/":
                result.append(folder[:-1])
        return result

    def getAllCourses(self):
        mainCoursesList = self._getMainCoursesList(self._getBs(COURSES_LIST_URL))
        result = []
        for course in mainCoursesList:
            deepCourseList = self._getDeepCourseList(course)
            if not deepCourseList is None:
                info(deepCourseList)
                result += deepCourseList
        return result

    def _getCourseUrl(self, course):
        return COURSES_LIST_URL % course

    def _getHtml(self, url):
        return urlfetch.fetch(url=url,deadline=60).content

    def _getBs(self, url):
        return BeautifulSoup(self._getHtml(url))

    def _getDeepCourseList(self, course):
        bs = self._getBs(COURSES_LIST_URL + course)
        if u"Course Sites" in [r.getText() for r in bs.findAll("h2")]:
            result = []
            # This course has sub-sites
            for a in bs.findAll("a"):
                link = a.attrs["href"]
                if "index.php" in link:
                    if link == 'Index.html':
                        link = COURSES_LIST_URL + course + '/' + link
                    result.append((course + " - " + a.getText(), link))
            return result
        else: 
            # This course has no sub-sites
            for a in bs.findAll("a"):
                linkText = a.getText()
                link = a.attrs["href"]
                if link == 'Index.html':
                    link = COURSES_LIST_URL + course + '/' + link
                if 'Main web page' in linkText or 'Course site' in linkText:
                    return [(course, link)]
            debug("Could not parse %s" % course)

    def _getExerciseList(self, html):
        # TODO find table
        # TODO parse all exercises: number, topic, upload url
        pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    c = Courses()
    for course in c.getAllCourses():
        debug(course)
