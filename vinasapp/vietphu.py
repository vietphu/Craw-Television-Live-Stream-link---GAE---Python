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
		foo = ".cdnviet.com/"
		mainurl = 'http://www.htvonline.com.vn/livetv'
		mainurl.encode('utf-8')
		opener = urllib2.build_opener()
		# filehandle = urllib.urlopen(mainurl)
		opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0')]
		# opener.addheaders.append( ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8') )
		# opener.addheaders.append( ('Accept-Encoding', 'gzip, deflate') )
		# opener.addheaders.append( ('Accept-Language', 'en-US,en;q=0.5') )
		# opener.addheaders.append( ('Connection', 'keep-alive') )
		# opener.addheaders.append( ('Host', 'htqjrpsv.cdnviet.com') )
		# opener.addheaders.append( ('Referer', 'http://www.htvonline.com.vn/js/jwplayer.flash.swf') )
		# opener.addheaders.append( ('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0') )
		filehandle = opener.open(mainurl).read()
		soup = BeautifulSoup(filehandle)
		i=0
		objchanel = []
		for anchor in soup.find_all('a',{ 'class':'mh-grids5-img'}):
		  logging.info('Link: %s', anchor['href'].encode('utf-8'))
		  # filechanel = urllib.urlopen(anchor['href'].encode('utf-8'))
		  filechanel = opener.open(anchor['href'].encode('utf-8')).read()
		  bufFilechanel = StringIO.StringIO(filechanel)
		  for lines in bufFilechanel.readlines():
			 if foo in lines:
				firstsign = lines.index('"') + 1
				lines = lines[firstsign:] 
				lastsign = lines.index('"')
				lines = lines[:lastsign]
				logging.info('[Index]: %s', i)
				logging.info('[Title]: %s', anchor['title'].encode('utf-8'))
				logging.info('[Lines]: %s', lines.encode('utf-8'))
				logging.info('[Img]: %s', anchor.find('img')['src'].encode('utf-8'))
				# objchanel.append({'id': i, 'title': anchor['title'],'lines': lines, 'img':anchor.find('img')['src']})
				i=i+1
		# objchanelpreload = json.dumps(objchanel)
		# jsonobjchanel = json.loads(objchanelpreload)
		# print json.dumps(jsonobjchanel, indent=4, sort_keys=True)
		# filehandle.close()

app = webapp2.WSGIApplication([
    ('/runcron', VietPhu)
], debug=True)