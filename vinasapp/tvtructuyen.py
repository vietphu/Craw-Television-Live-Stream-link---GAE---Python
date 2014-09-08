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

class Chanel(db.Model):
	name = db.StringProperty(indexed=False,default='')
	URLSrc = db.StringProperty(indexed=False,default='')
	img = db.StringProperty(indexed=False,default='')
	urls = db.TextProperty(required=False,default='')
	active = db.BooleanProperty(required=False,default=True)
	solution = db.IntegerProperty(indexed=False,default=1)   # solution to feed
	needfeed = db.BooleanProperty(indexed=False,default=True) # may be we need static link, so set this field to False

class VietPhu(webapp2.RequestHandler):
	user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
	headers={'User-Agent':user_agent,}
	
	#http://tivi12h.com/
	#http://xemtvhd.com/
	
	def get(self):
		chanelList=[
		# 'http://tivionline.vn/tivionline/vtv3.php',1,
		# 'http://xemtvhd.com/xemtvhd/vtvphuyen.php',1,
		# 'http://xemtvhd.com/xemtvhd/vtv6.php',1,
		# 'http://www.vtvplus.vn/index.php?option=com_vtv&view=channel&id=2',3,
		# 'http://vtvplay.vn/api/channel?streamid=11',4,"VTV3 HD",
		# 'http://vtvplay.vn/api/channel?streamid=1',4,"VTV1",
		# 'http://vtvplay.vn/api/channel?streamid=9',4,"VTV2",
		# 'http://vtvplay.vn/api/channel?streamid=12',4,"VTV4",
		# 'http://vtvplay.vn/api/channel?streamid=3',4,"VTV6",
		# 'http://vtvplay.vn/api/channel?streamid=10',4,"VTV9",
		# 'http://vtvplay.vn/api/channel?streamid=5',4,"TheThaoTV HD",
		# 'http://vtvplay.vn/api/channel?streamid=31',4,"BiBi",
		# 'http://vtvplay.vn/api/channel?streamid=6',4,"Bong Da TV HD",
		# 'http://vtvplay.vn/api/channel?streamid=4',4,"Kenh 14",
		# 'http://vtvplay.vn/api/channel?streamid=26',4,"Today TV",
		# 'http://vtvplay.vn/api/channel?streamid=13',4,"Start Sport",
		# 'http://vtvplay.vn/api/channel?streamid=7',4,"FOX Sport Plus HD",
		# 'http://vtvplay.vn/api/channel?streamid=24',4,"HTV7",
		# 'http://vtvplay.vn/api/channel?streamid=25',4,"HTV9",
		# 'http://vtvplay.vn/api/channel?streamid=19',4,"SCTV15",
		# 'http://vtvplay.vn/api/channel?streamid=20',4,"SCTV The Thao HD",
		# 'http://vtvplay.vn/api/channel?streamid=56',4,"Thuan Viet HD",
		'http://xemtvhd.com/xemtvhd/hbo.php',5,'HBO SD',
		'http://xemtvhd.com/xemtvhd/movies.php',3,'Star Movies',
		'http://xemtvhd.com/xemtvhd/star-movies-hd-2.php',3,'Star Movies HD',
		'http://xemtvhd.com/xemtvhd/vtc14.php',6,'VTC14',
		'http://xemtvhd.com/xemtvhd/vtc13.php',3,'VTC 13',#iTivi
		]
		 
		requestURL = ' '
		requestName = ' '
		requestSolution = 0
		for i in range(len(chanelList)):
			if (i%3) == 0:
				requestURL = chanelList[i]
			elif (i%3) == 1:
				requestSolution = chanelList[i]
			else:
				requestName = chanelList[i]
				self.feedSolution(requestURL,requestSolution,requestName)
				
	def feedSolution(self, requestURL, requestSolution, requestName):
		logging.info('[requestURL]: %s', requestURL)
		request=urllib2.Request(requestURL,None,self.headers) 
		response = urllib2.urlopen(request)
		data = response.read()
		urls = self.solutionCase(requestSolution,data)
		logging.info('[urls]: %s', urls)
		chanel = Chanel.get_or_insert(key_name = requestURL)
		chanel.urls = urls
		chanel.name = requestName
		chanel.put()
		
	def solutionCase(self, sl, data):
		detect_word_1 = "urlArry["
		detect_word_2 = ").setup({file:" #http://xemtvhd.com/xemtvhd/vtvphuyen.php
		detect_word_3 = "var responseText =" #http://xemtvhd.com/vtv6-online-vtv6-truc-tuyen-kenh-vtv6.html
		
		urls = '';
		bufFilechanel = StringIO.StringIO(data)
		if sl==1:
			for lines in bufFilechanel.readlines():
				if detect_word_1 in lines:
					if lines.index(detect_word_1) == 0:
						firstsign = lines.index("'") + 1
						lines = lines[firstsign:] 
						lastsign = lines.index("'")
						lines = lines[:lastsign]
						logging.info('[Lines]: %s', lines)
						urls+=lines
						urls+='#'
			return urls

		if sl==2:
			for lines in bufFilechanel.readlines():
				if detect_word_2 in lines:
					urls = lines
			return urls
			
		if sl==3:
			detect_word = "var responseText ="
			for lines in bufFilechanel.readlines():
				if detect_word in lines:
					firstsign = lines.index("http:")
					lines = lines[firstsign:] 
					lastsign = lines.index(";</") - 1
					lines = lines[:lastsign]
					urls = lines
			return urls
			
		if sl==4:
			for lines in bufFilechanel.readlines():
				logging.info('[Lines]: %s', lines)
				firstsign = lines.index('"') + 1
				lines = lines[firstsign:] 
				lastsign = lines.index('"') - 1
				lines = lines[:lastsign]
				urls = lines
			return urls
			
		if sl==5: #var urlArry = new Array();var typeArry = new Array();var num_of_urlArry;var index_of_urlArry;var start = true;var playing = false;index_of_urlArry = 0;urlArry[0]='http://m26.megafun.vn/ilive.m3u8?c=vstv036&token=-q3liG79ZNfa8GxrqzbctA&time=1402989866&q=high&type=tv&tk=a3ea1480b8a373a69f4ebb5fc37562b2';num_of_urlArry = urlArry.length;
			detect_word = "urlArry[0]='"
			for lines in bufFilechanel.readlines():
				if detect_word in lines:
					firstsign = lines.index(detect_word)+12
					lines = lines[firstsign:] 
					lastsign = lines.index("';num_of_urlArry =")
					lines = lines[:lastsign]
					urls = lines
					logging.info('[urls-solution5]: %s', urls)
			return urls	
		
		if sl==6: #jwplayer("myElement").setup({file: "rtmp://117.103.224.31/live/livestream",image: "tivionline-vn.png", stretching:'exactfit',width: '100%',height: '100%',autostart: true});
			detect_word = ").setup({file: "
			for lines in bufFilechanel.readlines():
				if detect_word in lines:
					firstsign = lines.index(detect_word) + 16
					lines = lines[firstsign:] 
					lastsign = lines.index(",image:") - 1
					lines = lines[:lastsign]
					urls = lines
					logging.info('[urls-solution6]: %s', urls)
			return urls	
			
		return None
		
app = webapp2.WSGIApplication([
    ('/runcron', VietPhu)
], debug=True)