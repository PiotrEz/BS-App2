import pika
import redis

IP_ADDRESS = '192.168.0.13'
PORT_REDIS = 6379
QUEUE_NAME = 'hello'
TTL = 60

while True:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=IP_ADDRESS))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME)

        def callback(ch, method, properties, body):
            r = redis.Redis(host=IP_ADDRESS, port=PORT_REDIS, db=0)
            total_keys = r.dbsize()
            r.set(total_keys, body, ex=TTL)
        channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()

