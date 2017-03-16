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
#/////////////////////
import sys
import requests
import time
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')

PHONE_URL = 'http://www.jihaoba.com/haoduan/%d/%s.htm'

def queryAll(province_city, city, code):
	try:	
		sUrl = PHONE_URL % (int(code), city)
		#print sUrl
		resp = requests.get(sUrl)
		html = resp.content.decode('utf-8')
		#print html
		soup = BeautifulSoup(html,'html.parser')
		ols = soup.body.find_all('ul')
		lis = ols[6].find_all('li')
		line = ''
		for li in lis:
			line = str(li)
			if 'hd-city01' in line:
				phone_prefix = str(li.getText().strip())
				body = phone_prefix
			elif 'hd-city02' in line:
				continue
			elif 'hd-city03' in line:
				city = str(li.getText().strip())
				province = province_city.get(str(city))
				body = '%s,%s,%s' % (body, province, city)
			elif 'hd-city04' in line:
				areacode = str(li.getText().strip())
				body = '%s,%s' % (body, areacode)
			elif 'hd-city06' in line:
				carrier = str(li.getText().strip())
				body = '%s,%s' % (body, carrier)
			elif 'hd-city07' in line:
				print body
				continue
			else :
				continue
					
	except Exception,e:
		print ''

def loopCity(filename, code):
	province_city = {}
	with open('/opt/push/zhuol/province-city') as p:
		lines = p.readlines()
		for line in lines:
			arr = line.strip().split(':')
			province = arr[0]
			cities = arr[1].split(',')
			for city in cities:
				province_city[city] = province
	with open(filename) as f:
		lines = f.readlines()
		for line in lines:
			city = line.strip().lower()
			time.sleep(3)
			queryAll(province_city, city, code)
if __name__=="__main__":
	loopCity(sys.argv[1], sys.argv[2])
