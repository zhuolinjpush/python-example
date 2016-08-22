#!/usr/bin/python

import sys
import time
import datetime
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import happybase
import types

connection = happybase.Connection('localhost',compat='0.90')
connection.open()
table = connection.table('test')
VER= 300

def query(row, column):
    values = table.cells(row, column, versions=VER)
    sum = 0
    for v in values:
        sum += int(v.encode('hex'),16)
    print sum

if __name__=='__main__':
    row = sys.argv[1]
    column = sys.argv[2]
    print 'row=',row, 'column=',column
    query(row, column)

    connection.close()
