############################ tmp producer ###############
import sys
from pykafka import KafkaClient
hosts_list = '172.16.111.111:9092'
def produce(topic_name, value):
    client = KafkaClient(hosts=hosts_list)
    print client
    topic = client.topics[topic_name]
    print topic
    producer = topic.get_sync_producer()
    producer.produce(value)

if __name__=="__main__":
    topic = sys.argv[1]
    value = ''
    print topic, value
    produce(topic, str(value))

########################### tmp consumer ###################
import json
from pykafka import KafkaClient
hosts = '172.16.111.111:9092'
client = KafkaClient(hosts=hosts)
#print client.topics
#topic = client.topics["mobile_num"]
#consumer = topic.get_balanced_consumer(consumer_group="test",zookeeper_connect='192.168.248.230:2181,192.168.248.175:2181,192.168.249.238:2181/kafka')
#for i in range(0, 10):
#    mes = consumer.consume()
#    print mes.value
