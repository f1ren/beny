#!/usr/bin/env python

from bs4 import BeautifulSoup

COURSES_LIST_URL = "http://physweb.bgu.ac.il/COURSES/"
COURSE_URL = "http://physweb.bgu.ac.il/COURSES/ProtoCourse/index.php?folder=%s#Home"

class Courses(object):
    def __init__(self):
        pass

    def getCoursesUrl(self):
        return COURSES_LIST_URL

    def getCoursesList(self, html):
        s = BeautifulSoup(html)
        result = []
        for a in s.findAll("a"):
            folder = a.getText()
            if folder[-1] == "/":
                result.append(folder[:-1])
        return result

    def getCourseUrl(self, course):
        return COURSES_LIST_URL % course

    def getExerciseList(self, html):
        s = BeautifulSoup(html)
        # TODO find table
        # TODO parse all exercises: number, topic, upload url

if __name__ == "__main__":
    ch = open(r"E:\projects\Beny\Server\Sandbox\BGU Physics Department.htm", "rb").read()
    c = Courses()
    c.getCoursesList(ch)
    ch = open(r"E:\projects\Beny\Server\Sandbox\Physics 3 - BGU Physics Department.htm", "rb").read()
    print c.getExerciseList(ch)
