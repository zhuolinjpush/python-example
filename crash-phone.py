#!/usr/bin/pythomn
# -*- coding:utf-8 -*-

import sys
import requests
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')

PHONE_URL = 'http://www.guisd.com/lb/%s/all/'

def queryAll(phone_prefix):
	try:	
		sUrl = PHONE_URL % phone_prefix
		#print sUrl
		resp = requests.get(sUrl)
		html = resp.content.decode('utf-8')
		soup = BeautifulSoup(html,'html.parser')
		tables = soup.find_all('table')
		#print tables
		for table in tables:
			for row in table.find_all('tr'):
				#print '-------------'
				tds = row.find_all('td')
				#print tds
				if len(tds) >= 6:
					code = tds[0].find('a').getText()
					provice = tds[1].getText()
					city = tds[2].getText()
					areacode = tds[3].getText()
					postcode = tds[4].getText()
					carrier = tds[5].getText()
					print '%s\t%s\t%s\t%s\t%s\t%s' % (code, provice, city, areacode, postcode, carrier)
					
	except Exception,e:
		print e


if __name__=="__main__":
	queryAll(sys.argv[1])
