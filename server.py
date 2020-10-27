#!/usr/bin/env python3
import pika
import sys
import uuid
import datetime
import time

rhost = "localhost"

credentials = pika.PlainCredentials('nick', 'nicolas')
parameters = pika.ConnectionParameters(host=rhost, virtual_host="/",
                                       credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='closet')
print('Waiting for Inventory')

def callback(ch, method, properties, body):
    response = body.decode('utf-8')
    print("Recieved: %s" % response)
    time.sleep(body.count(b'.'))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='closet')

channel.start_consuming()
