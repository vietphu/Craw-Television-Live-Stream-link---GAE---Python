
import logging
import webapp2
import urllib
import sys
import json
sys.path.insert(0,'libs')
#sys.path.append(os.path.join(os.path.dirname(__file__), "libs"))
from bs4 import BeautifulSoup
from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(60)

from google.appengine.ext import db

welcome = """
<html>
<body>
<p>
Welcome to the Vinasapp
<p>
<a href=http://vinasapp.com>Please go to main Vinasapp website</a>
</body>
</html>
"""

class Chanel(db.Model):
	id = db.IntegerProperty(required=False)
	img = db.StringProperty(indexed=False)
	urls = db.TextProperty(required=False)
	active = db.BooleanProperty(required=False,default=True)

class ListChanelHandler(webapp2.RequestHandler):
    def get(self):
		self.response.write(welcome)

app = webapp2.WSGIApplication([
    ('/', ListChanelHandler),
], debug=True)
