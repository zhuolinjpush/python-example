#1/usr/bin/env python
# -*- coding:utf-8 -*-


import sys
import time
import requests
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from elasticsearch import Elasticsearch
import happybase
import types
reload(sys)
sys.setdefaultencoding('utf-8')


es = Elasticsearch("172.16.1.1:19250")

searchsql2='{"fields":["imsi","phone"],"query":{"bool":{"must":[{"term":{"imsi":"%s"}}],"must_not":[],"should":[]}},"from":0,"size":20}'

def mSearchImsi(imsis):
	try :
		third_phone = {}
		sqls = []
		for imsi in imsis:
			sql = searchsql2 % imsi
			sqls.append(sql)
        	res = es.msearch(index='thrid_phone', body=sqls)
        	responses = res['responses']
		if len(responses) > 0:
			for r in responses:
				hits = r['hits']['hits']
				for hit in hits:
					fields = hit['fields']
					r_imsi = fields['imsi'][0] 
					r_phone = fields['phone']	
					third_phone[r_imsi] = r_phone
		return third_phone
	except Exception,e:
		return third_phone

def process(filename):
	f = open(filename)
	filelist = f.readlines()
	imsis = []
	lists = []
	for line in filelist:
		arr = line.strip().split('\t')
		if len(arr) < 3:
			continue
		imsi = arr[1].strip()
		imsis.append(imsi)
		lists.append(line.strip())
		if len(imsis) >= 200:
			res = mSearchImsi(imsis)
			for content in lists:
				array = content.split('\t')
				if res.has_key(array[1]):
					print "%s\t%s\t%s" % (array[0], array[1], res[array[1]])
				else :
					print content
			imsis = []
			lists = []
	if len(imsis) > 0:
		res = mSearchImsi(imsis)
		for content in lists:
                	array = content.split('\t')
                        if res.has_key(array[1]):
                        	print "%s\t%s\t%s" % (array[0], array[1], res[array[1]])
                        else :
                                print content

if __name__=="__main__":
	process(sys.argv[1])
