import sys
from elasticsearch import Elasticsearch

es = Elasticsearch("localhost:19250")

searchsql='{"query":{"bool":{"must":[{"term":{"appkey":"8103a4c1949"}},{"term":{"phone":"12345678911"}}]}},"size":1}'

def query():
	res = es.search(index='phone_v1', body=searchsql)
	for hit in res['hits']['hits']:
		_id = hit['_id']
		info = hit['_source']
		ukey = info['ukey']
		print 'es-data:%s:%s' % (_id, ukey)
		es.delete(index='phone_v1',id=_id)

if __name__=="__main__":
	query()

--------------------
#1/usr/bin/env python
# -*- coding:utf-8 -*-


import sys
import time
from elasticsearch import Elasticsearch

es = Elasticsearch("localhost:19290")

searchsql='{"fields":["appkey","msg_id","itime","msg_content"],"from":0,"size":10000,"query":{"bool":{"must":[{"term":{"appkey":"123"}},{"range":{"itime":{"gte":%d,"lte":%d}}}]}}}'
def query(start,end):
    sql = searchsql % (int(start),int(end))
    #print sql
    res = es.search(index='push_list_v1', body=sql)
    for hit in res['hits']['hits']:
        info = hit['fields']
        appkey = info['appkey']
        msgid = info['msg_id']
        itime = info['itime']
        msgcontent = info['msg_content']
        print '%s\t%s\t%s\t%s' % (appkey[0], msgid[0], itime[0], msgcontent[0])

if __name__=="__main__":
    query(int(time.mktime(time.strptime(sys.argv[1],'%Y%m%d'))),int(time.mktime(time.strptime(sys.argv[2],'%Y%m%d'))))
