
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

class Chanel(db.Model):
	id = db.IntegerProperty(required=False)
	img = db.StringProperty(indexed=False)
	urls = db.TextProperty(required=False)
	active = db.BooleanProperty(required=False,default=True)

class ListChanelHandler(webapp2.RequestHandler):
    def get(self):
		q = Chanel.all()
		response_data = []
		for p in q.run(limit=999):
			# logging.info('[id]: %s', p.id)
			# logging.info('[img]: %s', p.img)
			# logging.info('[urls]: %s', p.urls)
			# logging.info('[active]: %s', p.active)
			d = {}
			d['id']=p.id
			d['img']=p.img
			d['urls']=p.urls
			d['active']=p.active
			response_data.append(d)
		self.response.write(json.dumps(response_data))
		
app = webapp2.WSGIApplication([
    ('/listchanel', ListChanelHandler)
], debug=True)
