
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

#print json.dumps(jsonobjchanel, indent=4, sort_keys=True)
#filehandle.close()

class Chanel(db.Model):
	id = db.IntegerProperty(required=False)
	img = db.StringProperty(indexed=False)
	urls = db.TextProperty(required=False)
	active = db.BooleanProperty(required=False,default=True)

class ListChanelHandler(webapp2.RequestHandler):
    def get(self):
		q = Chanel.all()
		for p in q.run(limit=5):
			logging.info('[id]: %s', id)
			logging.info('[img]: %s', img)
			logging.info('[urls]: %s', urls)
			logging.info('[active]: %s', active)
		self.response.write(q)
		
app = webapp2.WSGIApplication([
    ('/', ListChanelHandler)
], debug=True)
