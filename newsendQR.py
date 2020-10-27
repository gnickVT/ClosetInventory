#!/usr/bin/env python3

import pika
import json
import sys
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

COUNT = 0

hostIP = sys.argv[1]

#credentials = pika.PlainCredentials('nick', 'nicolas')
#parameters = pika.ConnectionParameters(host="172.29.74.8", virtual_host="/", credentials = credentials)
									   
connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostIP))
channel = connection.channel()
channel.queue_declare(queue='closet')

channel.basic_publish(exchange='', routing_key='closet', body="green shirt")


class Handler(FileSystemEventHandler):
    def on_modified(self,event):
        # Whenever a new QR code is scanned clothing.txt is updated
        # This loop checks for changes to this file and will send the
        # item of clothing from the QR code to the database to be stored
        if event.src_path == "./clothing.txt":
            global COUNT
            if COUNT == 1:
                f = open("clothing.txt", "r")
                item = f.readline()
                f.close()
                payload = ('%s' % item)
                channel.basic_publish(exchange='',
                                      routing_key='closet',
                                      body=json.dumps({"action": "", "name": payload}))
                #channel.basic_ack(delivery_tag = method.delivery_tag)
                print("Changed Status of: %s" % item)
                COUNT = 0
            else:
                COUNT = COUNT+1


observer = Observer()
observer.schedule(Handler(), ".") #Watch local directory
observer.start()

try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    observer.stop()
    connection.close()

observer.join()
