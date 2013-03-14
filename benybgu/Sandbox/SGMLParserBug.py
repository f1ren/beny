import sgmllib

# XHTML is not supported in sgmllib
GOOD_HTML = "<br ><form name='aFrom'></form>"
BAD_HTML =  "<br/><form name='aFrom'></form>"

class MyParser(sgmllib.SGMLParser):
    def __init__(self, verbose=1):
        sgmllib.SGMLParser.__init__(self, verbose)
        self.hyperlinks = []

    def start_form(self, attrs):
        print "From found!"

p = MyParser()
p.feed(BAD_HTML)
p.feed(GOOD_HTML)
