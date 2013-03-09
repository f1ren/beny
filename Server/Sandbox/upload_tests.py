import base64
import mechanize
from bs4 import BeautifulSoup
import sys
import logging

FORMAT = '%(pathname)s %(lineno)d %(message)s'
logging.basicConfig(format=FORMAT)

logger = logging.getLogger("mechanize")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

def saveResp(resp, stage):
    lines = resp.readlines()
    open(r"E:\Projects\Beny\Server\temp%d.htm" % stage, "wb").write("".join(lines))

url = r"http://physweb.bgu.ac.il/SUBMISSIONS/Scripts_bgu/upload.php?exnum=1&path=13A_Physics3_est_segel/"
password = raw_input()
filename = r"E:\Dropbox\Uni\Physics3\empty.pdf"

br = mechanize.Browser()

# Authenticate upload page
br.addheaders.append(('Authorization', 'Basic %s' % base64.encodestring('%s:%s' % ("navatm", password))))
resp = br.open(url)
saveResp(resp, 1)

# Send file
br.select_form(name="fileForm")
br.form.add_file(open(filename,"rb"), 'text/plain', filename)
resp = br.submit()

# Fix <br/> since XHTML is not supported by SGMLParser used by mechanize
resp.set_data(resp.get_data().replace("<br/>", "<br>"))
saveResp(resp, 2)

br.set_response(resp)

# Confirm file
br.select_form(name="ConfirmForm")
resp = br.submit()
saveResp(resp, 4)
