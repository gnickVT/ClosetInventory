#!/usr/bin/env python

import sys
import bluetooth
import datetime
import time
import json
import ast
from ast import literal_eval
import pymongo
import pprint

from pymongo import MongoClient
from MongoDB import *
from LED import *

port = 0
backlog = 0
size = 0



def returnTime():
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
	return st

if(len(sys.argv) == 7):
	if(sys.argv[1] == "-p" and sys.argv[3] == "-b" and sys.argv[5] == "-z"):
		port = int(sys.argv[2])
		backlog = int(sys.argv[4])
		size = int(sys.argv[6])
else:
	print("Invalid: Input parameters")
	exit()

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

server_sock.bind(("",port))
server_sock.listen(1)
st = returnTime()
print("[" + st + "] " + "Created socket at " + " on port " + str(port))

while 1:
	bookCount = booksInDB()
	#print("number of books in the database: " + str(bookCount))
	setCounts(bookCount)
	st = returnTime()
	print("[" + st + "] " + "Listening for client connections")
	client_sock,address = server_sock.accept()
	st = returnTime()
	print ("[" + st + "] " + "Accepted client connection from " + str(address[0]) + " on port " + str(port))

	data = client_sock.recv(size)
	st = returnTime()
	n = data.decode("utf-8")
	n = ast.literal_eval(n)
	#print(isinstance(n, dict))
	print ("[" + st + "] " + "Received Payload: " + data.decode("utf-8"))
	if(n["Action"] == "ADD"):
		response = addFunction(n)
	elif(n["Action"] == "BUY"):
		response = buyFunction(n)
	elif(n["Action"] == "SELL"):
		response = sellFunction(n)
	elif(n["Action"] == "DELETE"):
		response = deleteFunction(n)
	elif(n["Action"] == "COUNT"):
		response = countFunction(n)
	elif(n["Action"] == "LIST"):
		response = listFunction(n)
		
	
	
	client_sock.send(response.encode())
	#print(response)

client_sock.close()
server_sock.close()

