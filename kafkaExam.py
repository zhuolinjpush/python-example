import logging
import csv
from StringIO import StringIO
try:
    import ujson as json
except ImportError:
    import json

from pandas import DataFrame
from pykafka import KafkaClient
from settings import kafka_consumer_group
from pykafka.balancedconsumer import OffsetType

zk_hosts = 
hosts = 
bootstrap_servers = hosts.split(',')

consumer = None
producer = None

def init_consumer(topic_name='user_location', consumer_group=kafka_consumer_group):
    client = KafkaClient(hosts=hosts)
    topic = client.topics[topic_name]
    consumer = topic.get_balanced_consumer(
        consumer_group=consumer_group,
        zookeeper_connect='',
        auto_offset_reset=OffsetType.LATEST
    )
    return consumer

def init_producer(topic_name=''):
    "init/re-init producer of topic"
    client = KafkaClient(hosts=hosts)
    topic = client.topics[topic_name]
    producer = topic.get_producer()
    return producer

def get_input_batch(consumer, batch_size=1000):
    meses = []
    for i in range(batch_size):
        mes = consumer.consume().value
        if mes:
            meses.append(mes)
    consumer.commit_offsets()
    return meses

def retry_if_any_error_reinit_consumer(exception):
    global consumer
    logging.error(exception)
    consumer.stop()
    consumer = init_consumer()
    return True

def get_input_df(consumer, batch_size=1000):
    meses = []
    for i in range(batch_size):
        mes = consumer.consume()
        if mes:
            meses.append(json.loads(mes.value))
    # input_jsons = [json.loads(mes.value, parse_int=str, parse_float=str) for mes in meses]
    consumer.commit_offsets()
    return DataFrame(meses)

def retry_if_any_error_reinit_producer(exception):
    global producer
    logging.error(exception)
    producer.stop()
    producer = init_producer()
    return True

# @retry(retry_on_exception=retry_if_any_error_reinit_producer, wait_fixed=3000, stop_max_attempt_number=3)
def write_df_to_kafka(df, producer, columns=, sep='\t'):
    """ write df as CSV to kafka thougth producer """
    result_buf = StringIO()
    df.to_csv(result_buf, sep=sep, na_rep=r'\N', quoting=csv.QUOTE_NONE, encoding='utf-8',
              header=False, index=False, mode='a+', date_format='%s', columns=columns)
    result_buf.seek(0)

    for line in result_buf:
        line = line.strip('\n')
        producer.produce(line)

def write_df_to_file(df, output_file, columns=, sep='\t', header=False):
    """ write df as CSV to local file """
    df.to_csv(output_file, sep=sep, na_rep=r'\N', quoting=csv.QUOTE_NONE, encoding='utf-8',
              header=header, index=False, mode='a+', date_format='%s', columns=columns)
