#!/usr/bin/env python

from google.appengine.api import urlfetch
from bs4 import BeautifulSoup
import urllib2
import logging
from logging import debug
import re

class Exercises(object):
    def __init__(self):
        pass

    def _parseExerciesTr(self, tr):
        tds = tr.findAll()
        texts = [td.getText() for td in tds]
        links = [td.a.attrs["href"] for td in tds if not td.a is None]
        if len(links) == 0:
            return None
        debug(links)
        return texts[0:3] + links[0:2] + [texts[5]] + [links[2]]

    def _getAllExercises(self, html):
        result = []
        bs = BeautifulSoup(html)
        for h2 in bs.findAll("h2"):
            if "Home Exercise" in h2.getText():
                table = h2.findNext("table")
                for tr in table.findAll("tr"):
                    result.append(self._parseExerciesTr(tr))
        return result

    def _getHtml(self, url):
        return urlfetch.fetch(url=url,deadline=60).content

    def getAllExercisesFromUrl(self, url):
        logging.info("Getting exercises from %s" % url)
        return self._getAllExercises(self._getHtml(url))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    html = open(r"E:\projects\Beny\benybgu\Sandbox\Physics 3 - BGU Physics Department.htm", "rb").read()
    exercises = Exersices()
    exs = exercises.getAllExercises(html)
    for ex in exs:
        print ex
