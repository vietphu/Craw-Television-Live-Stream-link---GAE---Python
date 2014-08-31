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

from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(1200)

class VietPhu(webapp2.RequestHandler):
    def get(self):
		foo = "urlArry["
		mainurl = 'http://tivionline.vn/tivionline/vtv3.php'
		chanelList=['http://tivionline.vn/tivionline/vtv3.php','http://tivionline.vn/tivionline/vtv2.php','http://tvtructuyen.net/xem/hbo.php']
		user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
		headers={'User-Agent':user_agent,} 
		
		for i in range(len(chanelList)):
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
app = webapp2.WSGIApplication([
    ('/runcron', VietPhu)
], debug=True)