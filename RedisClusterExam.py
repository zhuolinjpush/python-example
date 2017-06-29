import sys
from rediscluster import StrictRedisCluster

cluster_nodes = [{"host":"172.16.11.11", "port":16380}]

rc = StrictRedisCluster(startup_nodes=cluster_nodes, decode_responses=True)

def query(prefix):
	res = rc.keys(prefix)	
	sum = 0
	for k in res:
		ct = int(rc.get(k))
		print '%s\t%s' % (k, ct)


if __name__=="__main__":
	appkey = sys.argv[1]
	msgid = sys.argv[2]
	prefix = '%s-%s*' % (appkey,msgid)
	print prefix
	query(prefix)
