#!/usr/bin/env python

import datetime
import mechanize
import base64
import logging
import re

UPLOAD_URL = "http://physweb.bgu.ac.il/SUBMISSIONS/Scripts_bgu/upload.php?exnum=%s&path=%s/"

class PhysWeb(object):
    def __init__(self):
        self.br = mechanize.Browser()
        
    def _getUploadUrl(self, path, exnum):
        return UPLOAD_URL % (exnum, path)

    def _authenticate(self, url, username, password):
        self.br.addheaders.append(('Authorization',
            'Basic %s' % base64.encodestring('%s:%s' % (username, password))))
        return self.br.open(url)

    def _sendFile(self, filehandle, filename):
        self.br.select_form(name="fileForm")
        self.br.form.add_file(filehandle, 'text/plain', filename)
        return self.br.submit()

    def _confirmFile(self):
        self.br.select_form(name="ConfirmForm")
        return self.br.submit()

    def _XhtmlToHtml(self, xhtml):
        return xhtml.replace("<br/>", "<br>")

    def _wasFileSent(self, html):
        message = re.findall(r'<div class="heb">(.*?)<br />', html)[0]
        return hash(message) == 670043689

    def submitExercise(self, uname, password, path, exnum, exercise):
        #path = self._getCoursePath(course)
        url = self._getUploadUrl(path, exnum)

        self._authenticate(url, uname, password)
        resp = self._sendFile(exercise, "file.pdf")
        resp.set_data(self._XhtmlToHtml(resp.get_data()))
        self.br.set_response(resp)
        resp = self._confirmFile()
        assert self._wasFileSent(resp.get_data()), \
            "No confirmation message received"

if __name__ == "__main__":
    pw = PhysWeb()
    #print pw._getCoursePath("Thermo_I")
    #assert(pw._getCoursePath("Thermo_I") == "13A_Thermo_I_alo_segel")
    print pw._wasFileSent(open(r"E:\Projects\Beny\Server\Sandbox\temp4.htm", "rb").read())
