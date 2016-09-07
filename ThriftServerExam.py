#!/usr/bin/env python

import sys
import logging
sys.path.append('../gen-py')
from zoyare import statService
from zoyare.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
import socket

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datafmt='%a, %d %b %Y %H:%M:%S', filename='/opt/thrift-server/py-impl/local/message.log',filemode='a')

class ZoyareHandler:
	def __init__(self):
		print 'init'

	def save(self, value):
		try:
			#print 'save:%s' % value
			logging.info('data:%s' % value)
		except Exception,e:
			print e

handler = ZoyareHandler()
processor = statService.Processor(handler)
transport = TSocket.TServerSocket('localhost',18888)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print 'Starting python server...'
server.serve()
print 'done!'
