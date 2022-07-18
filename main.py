import pika
import redis
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("ip_Redis", help="Redis IP address")
parser.add_argument("ip_rabbit", help="RabbitMQ IP address")
parser.add_argument("-q", "--queue", default="hello", help="Redis queue name")
parser.add_argument("-p", "--app_port", default="3000", help="Define application port")
parser.add_argument("-rp", "--redis_port", default="6379", help="Redis Port")
parser.add_argument("-t", "--TTL", default="60", type=int, help="Define TTL, default: 60")
args = vars(parser.parse_args())

RABBIT_IP = args["ip_rabbit"]
REDIS_IP = args["ip_Redis"]
QUEUE_NAME = args["queue"]
APP_PORT = args["app_port"]
PORT_REDIS = args["redis_port"]
TTL = args["TTL"]


def callback(ch, method, properties, body):
    ID = random.random()
    r.set(ID, body, ex=TTL)


r = redis.Redis(host=REDIS_IP,port=PORT_REDIS,db=0)
size = r.dbsize()




connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBIT_IP))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
channel.start_consuming()






