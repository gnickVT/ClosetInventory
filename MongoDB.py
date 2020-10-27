from pymongo import MongoClient
from pprint import pprint

import sys
import bluetooth
import datetime
import time
import json
import ast
from ast import literal_eval


def returnTime():
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
	return st

client = MongoClient()
db = client.ClosetDB

posts = db.posts

def clothesInDB():
	bookCount = db.posts.find().count()
	return bookCount


def addFunction(object):
	payLoad = object
	payLoadMsg = payLoad["Msg"]
	payLoadBookInfo = payLoadMsg["Book Info"]
	nameOfBookForStock = payLoadBookInfo["Name"]
	post_id = ""
	returnText = ""

	payLoadBookInfo["stock"] = db.posts.find({"Name":nameOfBookForStock}).count()
	
	#post_id = posts.insert_one(payLoadBookInfo).inserted_id
	
	if(db.posts.find({"Name":nameOfBookForStock}).count()) == 0:
		payLoadBookInfo["stock"] = db.posts.find({"Name":nameOfBookForStock}).count()
		post_id = posts.insert_one(payLoadBookInfo).inserted_id
		st = returnTime()
		print("[" + st + "] " + "OK: Succesfully inserted. Book ID: " + str(post_id))
		returnText = ("OK: Succesfully inserted. Book ID: " + str(post_id))
		#print("Book is not in DB, add")
	else:
		st = returnTime()
		returnText = ("Add unsuccesful. Book already exists in database.")
	
	return returnText
	
def sellFunction(object):
	#print("called buy function")
	returnText = ""
	payLoad = object
	payLoadMsg = payLoad["Msg"]
	numberOfBooksToSell = int(payLoadMsg["Count"])
	payLoadBookInfo = payLoadMsg["Book Info"]
	nameOfBook = payLoadBookInfo["Name"]
	
	bookCount = db.posts.find({"Name":nameOfBook}).count() #check if book is in DB
	if bookCount > 0: #book exists add more
		#db.posts.update_one({"Name":nameOfBookForStock}, {'$inc':{"stock": 1}})
		post_id = db.posts.find_one({"Name":nameOfBook})
		if ((int(post_id["stock"])) > 0) and int(post_id["stock"]) > numberOfBooksToSell:
			db.posts.update_one({"Name":nameOfBook}, {'$inc':{"stock": -numberOfBooksToSell}})
			post_id = db.posts.find_one({"Name":nameOfBook})
			returnText = ("OK: Sell succesful, current book count: " + str(post_id["stock"]))
		else:
			returnText = ("Sell unsuccesful: Sell request too large. Or no more of the book in stock")
	else:
		returnText = "Sell unsuccesful: No book with that name exists in the database."
	
	return returnText
	
def deleteFunction(object):
	#print("called delete function")
	returnText = ""
	payLoad = object
	payLoadMsg = payLoad["Msg"]
	payLoadBookInfo = payLoadMsg["Book Info"]
	nameOfBook = payLoadBookInfo["Name"]
	authorOfBook = payLoadBookInfo["Author"]
	
	deleted = posts.delete_one({"Name":nameOfBook, "Author":authorOfBook})
	#print(deleted.deleted_count)
	
	if(deleted.deleted_count == 0):
		returnText = "Delete unsuccesful. No book with that name/author exists in the database."
	else:
		returnText = "OK: Succesfully deleted."
	
	return returnText

def buyFunction(object):
	#print("called buy function")
	returnText = ""
	payLoad = object
	payLoadMsg = payLoad["Msg"]
	numberOfBooksToBuy = int(payLoadMsg["Count"])
	payLoadBookInfo = payLoadMsg["Book Info"]
	nameOfBook = payLoadBookInfo["Name"]
	
	bookCount = db.posts.find({"Name":nameOfBook}).count() #check if book is in DB
	if bookCount > 0: #book exists add more
		#db.posts.update_one({"Name":nameOfBookForStock}, {'$inc':{"stock": 1}})
		db.posts.update_one({"Name":nameOfBook}, {'$inc':{"stock": numberOfBooksToBuy}})
		post_id = db.posts.find_one({"Name":nameOfBook})
		
		returnText = ("OK: Buy succesful, current book count: " + str(post_id["stock"]))
	else:
		returnText = "Buy unsuccesful: No book with that name exists in the database."
	
	return returnText

def countFunction(object):
	payLoad = object
	payLoadMsg = payLoad["Msg"]
	payLoadBookInfo = payLoadMsg["Book Info"]
	nameOfBook = payLoadBookInfo["Name"]
	
	bookCount = db.posts.find({"Name":nameOfBook}).count()
	returnText = ""
	
	if(bookCount > 0):
		post_id = db.posts.find_one({"Name":nameOfBook})
		#print(post_id["stock"])
		returnText = ("OK: " + str(post_id["stock"])+ " books in stock.")
	else:
		returnText = "Unsuccesful. No book with that name exists in the database."
	return returnText

def listFunction(object):
	listToReturn = list(db.posts.find())
	return str(listToReturn)
