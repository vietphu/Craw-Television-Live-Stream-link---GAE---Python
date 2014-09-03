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

from google.appengine.ext import db

from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(1200)

# def chanellist_key(chanellist_name='default_chanellist'):
    # return db.Key('ChanelListDB', chanellist_name)

class Chanel(db.Model):
	id = db.IntegerProperty(required=False)
	img = db.StringProperty(indexed=False)
	urls = db.TextProperty(required=False)
	active = db.BooleanProperty(required=False,default=True)

class VietPhu(webapp2.RequestHandler):
    def get(self):
		foo = "urlArry["
		mainurl = 'http://tivionline.vn/tivionline/vtv3.php'
		chanelList=[
		'http://tivionline.vn/tivionline/vtv3.php',
		'http://tivionline.vn/tivionline/vtv2.php',
		'http://tvtructuyen.net/xem/hbo.php',
		'http://tvtructuyen.net/xem/vtv1.php',
		'http://tvtructuyen.net/xem/vtv2.php', #always show vtv3
		'http://tvtructuyen.net/xem/vtv4.php',
		'http://tvtructuyen.net/xem/vtv6.php',
		]
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
			chanel = Chanel(key_name = chanelList[i])
			chanel.id = i
			chanel.urls = urls
			chanel.put()
			
app = webapp2.WSGIApplication([
    ('/runcron', VietPhu)
], debug=True)