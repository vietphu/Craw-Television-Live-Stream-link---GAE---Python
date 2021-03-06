#appcfg.py --oauth2 update myapp/
#appcfg.py --no_cookies --email=vinasapp1@gmail.com update ./
#dinhvietphu@gmail.com vinasapp
#vinasapp1@gmail.com vinasapp2
#vinasapp4@gmail.com vinasapp4
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
		
		#foreign
		'http://xemtvhd.com/xemtvhd/hbo.php',5,'HBO SD',
		'http://xemtvhd.com/xemtvhd/movies.php',3,'Star Movies',
		'http://xemtvhd.com/xemtvhd/star-movies-hd-2.php',3,'Star Movies HD',
		'http://xemtvhd.com/xemtvhd/arirang.php',7,'Arirang',
		'http://xemtvhd.com/xemtvhd/music-box.php',8,'Music box TV',
		'http://xemtvhd.com/xemtvhd/cinemax.php',3, 'Cinemax',
		# 'http://tvtructuyen.net/xem/cinemax.php',1,'Cinemax',
		'http://xemtvhd.com/xemtvhd/carton-cn.php',8,'CNN',
		'http://xemtvhd.com/xemtvhd/disney.php',1,'Disney',
		'http://tvtructuyen.net/xem/dicovery.php',1,'Dicovery chanel',
		
		#VTV
		'http://tvtructuyen.net/xem/vtv1.php',1,'VTV1',
		'http://tvtructuyen.net/xem/vtv2-3.php',12,'VTV2',
		'http://tvtructuyen.net/xem/vtv4-2.php',1,'VTV4',
		'http://tvtructuyen.net/xem/vtv6.php',1,'VTV6',
		'http://tvtructuyen.net/xem/vtv9-3.php',7,'VTV9',
		
		
		#VTC
		'http://xemtvhd.com/xemtvhd/vtc14.php',6,'VTC14',
		'http://xemtvhd.com/xemtvhd/vtc13.php',3,'VTC 13',#iTivi
		'http://xemtvhd.com/xemtvhd/vtc11-2.php',1,'VTC 11',#Kids TV
		'http://xemtvhd.com/xemtvhd/vtc3.php',3,'VTC3',
		'http://tvtructuyen.net/xem/vtc-hd3vtc.php',1,'VTC3 HD',
		'http://xemtivihd.vn/vtc-2-kenh-cong-nghe-thong-tin',7,'VTC2',
		'http://tvtructuyen.net/xem/vtc-hd1vtc.php',1,'VTC1 HD',
		'http://tvtructuyen.net/xem/vtc7-7.php',7,'VTC7-Today TV',
		
		#vietnam
		# 'http://xemtvhd.com/xemtvhd/vinhlong1.php',1,'Vinh Long 1',
		'http://xemtvhd.com/xemtvhd/anninh.php',3,'An ninh TV',
		'http://xemtvhd.com/xemtvhd/qpvn.php',7,'QPVN',
		'http://xemtvhd.com/xemtvhd/sctvhai.php',7,'SCTV Hai',
		'http://xemtvhd.com/xemtvhd/hanoi2.php',1,'Ha Noi 2', 
		'http://xemtvhd.com/xemtvhd/mtvviet.php',1,'MTV Viet',
		#http://tivi12h.com/mkt-online-kenh-giai-tri.php online, check to get this source, really interesting in
		#http://tivi12h.com/viet-mtv-kenh-viet-mtv-online.php
		'http://xemtvhd.com/xemtvhd/thuanviet-hd.php',1,'Thuan Viet HD',
		'http://xemtvhd.com/xemtvhd/fnbc.php',1,'FNBC',
		'http://tvtructuyen.net/xem/binhduong2.php',6,'Binh Duong 2',
		'http://tvtructuyen.net/xem/binhphuoc1.php',11,'Binh Phuoc 1',
		'http://tvtructuyen.net/xem/binhphuoc2.php',11,'Binh Phuoc 2',
		'http://tvtructuyen.net/xem/baria-vungtau.php',11,'Ba Ria - Vung Tau',
		'http://tvtructuyen.net/xem/mtvviet.php',8,'MTV Viet',
		'http://tvtructuyen.net/xem/v-music-viet.php',11,'VMusic Viet',
		'http://tvtructuyen.net/xem/vpop.php',7,'VPop',
		'http://tvtructuyen.net/xem/nct.php',11,'NCT',
		# 'http://tvtructuyen.net/xem/phimviet-2.php',1,'Phim viet',
		'http://tvtructuyen.net/xem/vovtv.php',1,'VOV TV',
		'http://tvtructuyen.net/xem/vtvcantho1.php',7,'VTV CanTho1',
		'http://tvtructuyen.net/xem/vtvcantho2.php',7,'VTV CanTho2',
		
		#HTV
		# 'http://xemtvhd.com/xemtvhd/htv3-mkt1.php?sv=m26.megafun.vn',9,'HTV3',
		# 'http://xemtvhd.com/xemtvhd/htv7.php',9, 'HTV7',
		# 'http://vtvplay.vn/api/channel?streamid=24',4,"HTV7",
		# 'http://vtvplay.vn/api/channel?streamid=25',4,"HTV9",
		'http://vpstesst.blogspot.com/2014/02/h9.html?sv=m7.megafun.vn',10,'HTV9',
		'http://xemtvhd.com/xemtvhd/htv-thethao.php',3,'HTV Theo Thao',
		
		
		#VTVplay
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
		# 'http://vtvplay.vn/api/channel?streamid=19',4,"SCTV15",
		# 'http://vtvplay.vn/api/channel?streamid=20',4,"SCTV The Thao HD",
		# 'http://vtvplay.vn/api/channel?streamid=56',4,"Thuan Viet HD",
		
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
				try:
				  self.feedSolution(requestURL,requestSolution,requestName)
				except: 
				  pass
				
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
			detect_word = "urlArry["
			for lines in bufFilechanel.readlines():
				if detect_word in lines:
					if lines.index(detect_word) == 0:
						firstsign = lines.index("'") + 1
						lines = lines[firstsign:] 
						lastsign = lines.index("'")
						lines = lines[:lastsign]
						logging.info('[Lines]: %s', lines)
						urls+=lines
						urls+=','
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
		if sl==7: #jwplayer("myElement").setup({file: "rtmp://117.103.224.31/live/livestream",image: "tivionline-vn.png", stretching:'exactfit',width: '100%',height: '100%',autostart: true});
			detect_word = "file: \""
			for lines in bufFilechanel.readlines():
				if detect_word in lines:
					firstsign = lines.index(detect_word) + 7
					lines = lines[firstsign:] 
					lastsign = lines.index("\",")
					lines = lines[:lastsign]
					urls = lines
					logging.info('[urls-solution7]: %s', urls)
			return urls
		
		if sl==8: #<iframe frameborder="no" height="100%" scrolling="no" title="music box" src="htv.php?sv=rtmp://musicbox.cdnvideo.ru/musicbox-live/musicboxtv.sdp" width="100%"></iframe>
			detect_word = "src=\"htv.php?"
			for lines in bufFilechanel.readlines():
				if detect_word in lines:
					firstsign = lines.index("sv=") + 3
					lines = lines[firstsign:] 
					lastsign = lines.index("\" width=")
					lines = lines[:lastsign]
					urls = lines
					logging.info('[urls-solution8]: %s', urls)
			return urls
		
		if sl==9: #var responseText = "http://"+sv+"/ilive.m3u8?c=vstv075&token=TEfnZB2F38QfZN0w1DLQYA&time=1403538641&q=medium&type=tv&tk=a3ea1480b8a373a69f4ebb5fc37562b2,http://frdlzsmb.cdnviet.com/psczntp/_definst_/htv3.360p.stream/playlist.m3u8";
			detect_word = "var responseText"
			for lines in bufFilechanel.readlines():
				if detect_word in lines:
					firstsign = lines.index("http:")
					lines = lines[firstsign:] 
					lastsign = lines.index("\";")
					lines = lines[:lastsign]
					lines.replace("\"+sv+\"", "m26.megafun.vn");
					urls = lines
		
		if sl==10: #var responseText = "http://"+sv+"/ilive.m3u8?c=vstv009&q=medium&type=tv&token=RDlwV-uUJSliZtUDbmbe9g&time=1410329237&gcId=1376442&userId=8&deviceId=630763&deviceType=5&location=NA&requestTime=1410242837806&pkg=pkg1,http://m26.megafun.vn/ilive.m3u8?c=vstv009&token=uN4b1Vt2Rq3bYqiuZqCASg&time=1403538639&q=medium&type=tv&tk=a3ea1480b8a373a69f4ebb5fc37562b2,rtmp://m22.megafun.vn/hctv/vstv009";
			detect_word = "var responseText"
			for lines in bufFilechanel.readlines():
				if detect_word in lines:
					firstsign = lines.index("http:")
					lines = lines[firstsign:] 
					lastsign = lines.index("\";")
					lines = lines[:lastsign]
					lines.replace("\"+sv+\"", "m7.megafun.vn");
					urls = lines
			return urls
			
		if sl==11: #streamer: "rtmp://113.161.180.136/live", file: "thbp1.tv",
			detect_word = "streamer: \""
			for lines in bufFilechanel.readlines():
				if detect_word in lines:
					firstsign = lines.index(detect_word) + 11
					prefix = lines[firstsign:] 
					lastsign = prefix.index("\",")
					prefix = prefix[:lastsign]
					
					firstsign = lines.index("file: \"") + 7
					suffix = lines[firstsign:]
					lastsign = suffix.index("\",\n")
					suffix = suffix[:lastsign]
					
					urls = prefix + "/" + suffix
			return urls
		
		if sl==12: #streamer: "rtmp://m22.megafun.vn/hctv", file: sv, primary: "flash",
			detect_word = "streamer: \""
			for lines in bufFilechanel.readlines():
				if detect_word in lines:
					firstsign = lines.index(detect_word) + 11
					prefix = lines[firstsign:] 
					lastsign = prefix.index("\",")
					prefix = prefix[:lastsign]
					
					urls = prefix + "/vstv017"
			return urls
			
		return None
		
app = webapp2.WSGIApplication([
    ('/runcron', VietPhu)
], debug=True)