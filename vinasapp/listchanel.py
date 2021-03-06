
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
from tvtructuyen import Chanel

class ListChanelHandler(webapp2.RequestHandler):
    def get(self):
		q = Chanel.all()
		response_data = []
		i=0;
		for p in q.run(limit=999):
			# logging.info('[id]: %s', p.id)
			# logging.info('[img]: %s', p.img)
			# logging.info('[urls]: %s', p.urls)
			# logging.info('[active]: %s', p.active)
			d = {}
			# d['id']=p.id
			d['key_name']=p.key().name()
			# logging.info('[key_name==========]: %s', d['key_name'])
			d['name']=p.name
			# d['img']=p.img
			if (i%2) == 0:
				d['img']='http://img.htvonline.com.vn/livetv/16062014/vtv3_20711402902808.png'
			else:
				d['img']='http://img.htvonline.com.vn/livetv/18052014/star-movies-hd--edited_75921400346206.png'
			d['urls']=p.urls
			d['active']=p.active
			response_data.append(d)
			i=i+1
		self.response.write(json.dumps(response_data))

class APIList(webapp2.RequestHandler):
    def get(self):
		api_links = [
			"http://vinasapp.appspot.com/listchanel",
			"http://vinasapp1.appspot.com/listchanel",
			"http://vinasapp4.appspot.com/listchanel",
			"http://vinasapp5.appspot.com/listchanel",
		]
		self.response.write(json.dumps(api_links))

		
app = webapp2.WSGIApplication([
    ('/listchanel', ListChanelHandler),
	('/apilist', APIList),
], debug=True)
