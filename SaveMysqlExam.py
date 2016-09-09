#!/usr/bin/python

import sys
import oursql
import time

myconf = ['localhost', 3306, 'stat', '123', 'statdb']

class Handler():
	def __init__(self):
		self.myclient = oursql.Connection(host=myconf[0], port=myconf[1], user=myconf[2], passwd=myconf[3], db=myconf[4], charset='utf8')
	
	def process(self, filename, itime, hour):
		sql = "insert into test (appkey,package,itime,hour_%d) values(?,?,?,?) on duplicate key update hour_%d=?" % (hour, hour)
		rows = []
		with open(filename) as f:
			filelines = f.readlines()
			for line in filelines:
				#print line
				arr = line.strip().split('\t')
				rows.append((arr[0].strip(),arr[1].strip(),itime,int(arr[3]),int(arr[3])))
			if len(rows) > 0:
				self.saveBatch(sql, rows)
				
	
	def saveBatch(self, sql, rows):
		try :
			print sql
			start = time.time()
			lens = len(rows)
			inss = list(rows)
			index = 0
			batch = 1000
			cursor = self.myclient.cursor()
			while index < lens:
				end_idx = index + batch
				cursor.executemany(sql, inss[index:end_idx])
				print 'syns rows[%s:%s] ok.' % (index, end_idx)
				index = end_idx
			cursor.close()	
			end = time.time()
			print 'save %s cost %s' % (lens, int(end - start))
		except Exception,e:
			print e	
		finally:
			self.close()

	def close(self):
		if self.myclient != None:
			self.myclient.close();

if __name__=="__main__":
	filename = sys.argv[1]
	ihour = sys.argv[2]
	itime = int(ihour[0:8])
	hour = int(ihour[8:10])
	handler = Handler()
	handler.process(filename, itime, hour)
