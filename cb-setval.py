#!/usr/bin/python


import sys
from couchbase.bucket import Bucket

cb = Bucket('couchbase://localhost/realtime-stats',password='123')

def query(key):
	res = cb.get(key).value
	print res

def setVal(key,val):
	cb.upsert(key, val)

if __name__=="__main__":
	key = sys.argv[1]
	val = int(sys.argv[2])
	setVal(key,val)
	query(key)
