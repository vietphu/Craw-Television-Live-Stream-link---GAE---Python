#!/usr/bin/python
import logging
import webapp2
import sys
import urllib
import urllib2
import json
import StringIO
sys.path.insert(0,'libs')
from bs4 import BeautifulSoup

from google.appengine.ext import ndb

from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(1200)

def chanellist_key(chanellist_name='default_chanellist'):
    return ndb.Key('ChanelListDB', chanellist_name)

class Chanel(ndb.Model):
    # key_name = ndb.StringProperty(indexed=True)
	id = ndb.StringProperty(required=True)
	name = ndb.StringProperty(required=True)
	img = ndb.StringProperty(indexed=False)
	urls = ndb.TextProperty(required=True)
    # date = ndb.DateTimeProperty(auto_now_add=True)

class VietPhu(webapp2.RequestHandler):
    def get(self):
		foo = "urlArry["
		mainurl = 'http://tivionline.vn/tivionline/vtv3.php'
		chanelList=['http://tivionline.vn/tivionline/vtv3.php','http://tivionline.vn/tivionline/vtv2.php','http://tvtructuyen.net/xem/hbo.php']
		user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
		headers={'User-Agent':user_agent,} 
		
		for i in range(len(chanelList)):
			urls = '';
			logging.info('[chanelList[i]]: %s', chanelList[i])
			request=urllib2.Request(chanelList[i],None,headers) 
			response = urllib2.urlopen(request)
			data = response.read()
			bufFilechanel = StringIO.StringIO(data)
			for lines in bufFilechanel.readlines():
				if foo in lines:
					if lines.index(foo) == 0:
						firstsign = lines.index("'") + 1
						lines = lines[firstsign:] 
						lastsign = lines.index("'")
						lines = lines[:lastsign]
						logging.info('[Lines]: %s', lines)
						urls+='#'
						urls+=lines
			logging.info('[urls]: %s', urls)
			# chanel = Chanel(parent=chanellist_key())
			chanel = Chanel.get_by_key_name(chanelList[i],parent=chanellist_key())
			if chanel is None:
				chanel = Chanel(key_name = chanelList[i],parent=chanellist_key())
				chanel.name = chanelList[i]
				chanel.urls = urls
				chanel.put()
			else:
				chanel.name = chanelList[i]
				chanel.urls = urls
				chanel.put()
app = webapp2.WSGIApplication([
    ('/runcron', VietPhu)
], debug=True)