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
