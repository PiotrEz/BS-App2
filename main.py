import pika
import redis
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("--ip_redis", help="Redis IP address", type=str, required=True)
parser.add_argument("--ip_rabbitmq", help="RabbitMQ IP address", type=str, required=True)
parser.add_argument("-q", "--queue", default="hello", help="Redis queue name")
parser.add_argument("-p", "--app_port", default="3000", help="Define application port")
parser.add_argument("-rp", "--redis_port", default="6379", help="Redis Port")
parser.add_argument("-rmp", "--rabbitmq_port", default="5672", type=str, help="RabbitMQ Port")
parser.add_argument("-t", "--TTL", default="60", type=int, help="Define TTL, default: 60")
parser.add_argument("-rmqu", "--rabbitmq_user", default="guest", type=str, help="Define RabbitMQ user name")
parser.add_argument("-rmqp", "--rabbitmq_password", default="guest", type=str, help="Define RabbitMQ user password")
args = parser.parse_args()

RABBIT_IP = args.ip_rabbitmq
USER_NAME = args.rabbitmq_user
USER_PASS = args.rabbitmq_password
RABBITMQ_PORT=args.rabbitmq_port
QUEUE_NAME=args.queue
TTL=args.TTL
PORT_REDIS=args.redis_port

def callback(ch, method, properties, body):
    ID = random.random()
    r.set(ID, body, ex=TTL)

r = redis.Redis(host=args.ip_redis,port=PORT_REDIS,db=0)
print ("Connected")
size = r.dbsize()


credentials = pika.PlainCredentials(USER_NAME, USER_PASS)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBIT_IP,port=RABBITMQ_PORT,credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
channel.start_consuming()






