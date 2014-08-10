#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import urllib
import sys
import json
sys.path.insert(0,'libs')
#sys.path.append(os.path.join(os.path.dirname(__file__), "libs"))
from bs4 import BeautifulSoup
from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(45)


#print json.dumps(jsonobjchanel, indent=4, sort_keys=True)
#filehandle.close()

class MainHandler(webapp2.RequestHandler):
    def get(self):
		foo = ".cdnviet.com/"
		mainurl = 'http://www.htvonline.com.vn/livetv'
		#mainurl.encode('utf-8')
		filehandle = urllib.urlopen(mainurl)

		soup = BeautifulSoup(filehandle)
		i=0
		objchanel = []
		for anchor in soup.find_all('a',{ 'class':'mh-grids5-img'}):
		  filechanel = urllib.urlopen(anchor['href'].encode('utf-8'))
		  for lines in filechanel.readlines():
			  if foo in lines:
				firstsign = lines.index('"') + 1
				lines = lines[firstsign:] 
				lastsign = lines.index('"')
				lines = lines[:lastsign]
				#print i,anchor['title'], lines, anchor.find('img')['src']
				#objchanel.append({'id': i, 'title': anchor['title'],'lines': lines, 'img':anchor.find('img')['src']})
				objchanel = anchor.find('img')['src']
				i=i+1
		# objchanelpreload = json.dumps(objchanel)
		# jsonobjchanel = json.loads(objchanelpreload)
		self.response.write(objchanel)
		
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
