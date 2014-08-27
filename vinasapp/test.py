#!/usr/bin/python
import logging
import sys
import urllib
import json
sys.path.insert(0,'libs')
from bs4 import BeautifulSoup

foo = ".cdnviet.com/"
mainurl = 'http://www.htvonline.com.vn/livetv'
mainurl.encode('utf-8')
filehandle = urllib.urlopen(mainurl)

soup = BeautifulSoup(filehandle)
i=0
objchanel = []
for anchor in soup.find_all('a',{ 'class':'mh-grids5-img'}):
  logging.info('Link: %s', anchor['href'].encode('utf-8'))
  # filechanel = urllib.urlopen(anchor['href'].encode('utf-8'))
  # for lines in filechanel.readlines():
     # if foo in lines:
        #firstsign = lines.index('"') + 1
        #lines = lines[firstsign:] 
        #lastsign = lines.index('"')
        #lines = lines[:lastsign]
        #print i,anchor['title'], lines, anchor.find('img')['src']
        # objchanel.append({'id': i, 'title': anchor['title'],'lines': lines, 'img':anchor.find('img')['src']})
        # i=i+1
# objchanelpreload = json.dumps(objchanel)
# jsonobjchanel = json.loads(objchanelpreload)
# print json.dumps(jsonobjchanel, indent=4, sort_keys=True)
# filehandle.close()
