
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
os.environ["NLS_LANG"] = "German_Germany.UTF8"
import datetime
import pika
import logging

filen = sys.argv[1]
logging.basicConfig(level=logging.INFO, filename='./time.log', format='%(asctime)s %(levelname)s %(message)s')

def import_all(fileName) :
    mq_host = '127.0.0.1'
    logging.info("file name is %s"%fileName)
    f = open(fileName)
    fileList = f.readlines()
    line_count = len(fileList)
    logging.info("line count is %d"%line_count)
    if (line_count > 0) :
        credentials = pika.PlainCredentials('test', 'test123')
        connection = pika.BlockingConnection(pika.ConnectionParameters( mq_host, 5672, '/', credentials))
        channel = connection.channel()
        logging.info('init mq conn ok')
        for fileLine in fileList :
            try :
                channel.basic_publish(exchange='fix-ex',
                                  routing_key='fix-rkey',
                                  body=fileLine
                                 )
             except Exception,e:
                    print e       
             line_count = line_count-1
        channel.close()
        connection.close()
        logging.info('close mq conn ok')
        logging.info('push over')
    f.close()

if __name__ == "__main__":
    import_all(filen)
