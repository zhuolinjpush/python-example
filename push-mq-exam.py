import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
os.environ["NLS_LANG"] = "German_Germany.UTF8"
import datetime
import pika
import logging
import chardet

logging.basicConfig(level=logging.INFO, filename='./log.msglc', format='%(asctime)s %(levelname)s %(message)s')

def import_all(fileName) :
    mq_host = '192.168.249.174'
    logging.info("file name is %s"%fileName)
    cc = 0
    credentials = pika.PlainCredentials('developer', 'DeveLoper_MQ')
    connection = pika.BlockingConnection(pika.ConnectionParameters( mq_host, 5672, '/', credentials))
    channel = connection.channel()
    logging.info('Init mq conn ok')
    regex_error = 'data:'
    with open(fileName) as f:
        fileList = f.readlines()
        for fileLine in fileList :
            index = fileLine.find(regex_error)
            if( index <> -1):
                line = fileLine[index + len(regex_error):]
                try:
                    channel.basic_publish(exchange='fix-ex-msgcycle',routing_key='fix-rk-msgcycle',body=line)        
                    cc = cc + 1
                    if (cc % 1000) == 0:
                        logging.inf0('push %d' % cc)
                except Exception,e:
                    connection = pika.BlockingConnection(pika.ConnectionParameters( mq_host, 5672, '/', credentials))
                    channel = connection.channel()
                    logging.info('ReInit mq conn ok')
    f.close()
    channel.close()
    connection.close()
    logging.info('close mq conn ok')
    logging.info('push over')

if __name__ == "__main__":
    filename = sys.argv[1]
    import_all(filename)
