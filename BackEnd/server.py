#!/usr/bin/env python3

import socket
import threading
import time
import sys
import os
import sqlite3
import pickle
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

SERVER_IP = "0.0.0.0"
SERVER_PORT = 10002

class Server:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connections = [] # Temporary list to stock conections, easier to read than database

	def __init__(self):
		self.sock.bind((SERVER_IP, SERVER_PORT))
		self.sock.listen(1)
		self.goSQL()
		self.getConnection()

	def goSQL(self):
		self.conn = sqlite3.connect(":memory:", check_same_thread = False) # Using :memory: pour le moment, eviter de recréer un fichier .db chaque fois
		self.cursor = self.conn.cursor()

		try:
			self.cursor.execute("""CREATE TABLE User_Info (
				name text,
				lastname text,
				password text,
				email text,
				phonenumer text,
				zipCode bigint
				)""")
			print("Database User_Info créée")
		except:
			print("La table User_Info existe déjà")
		
		try:
			self.cursor.execute("""CREATE TABLE Seller_Info (
				name text,
				lastname text,
				password text,
				email text,
				phonenumber text,
				zipCode bigint,
				stock bigint,
				price real,
				openingHours text
				)""")
			print("Database Seller_Info créée")
		except:
			print("La table Seller_Info existe déjà")


	def getConnection(self):
		while True:
			c, a = self.sock.accept()
			print(str(a[0]) + ":" + str(a[1]) + " vient de se connecter")
			c.send(b"Bienvenue chez Agreez\n\n")
			self.connections.append(c)
			clientThread = threading.Thread(target=self.handleEachUser, args=(c,))
			clientThread.daemon = True
			clientThread.start()


	def handleEachUser(self, c):
		typeOfUser = c.recv(1024)
		action = c.recv(1024)
		[self.login(c) if action == b"connection" else self.createAccount(c)]

	def login(self, c):
		compressed_data = c.recv(1024)
		data = pickle.loads(compressed_data)
		typeOfUser = data[0]
		email = data[1]
		password = data[2]
		if self.checkOK(typeOfUser, email, password):
			print("User logged in as %s" %email)
		else:
			print("Wrong Username")

	def checkOK(self, typeOfUser, email, password):
		#print("check : type = %s, email = %s, password = %s" % (typeOfUser, email, password))
		database = "User_Info" if typeOfUser == "Client" else "Seller_Info"
		#print("email: ", email)
		#email = str(email, "utf-8")
		#password = str(password, "utf-8")
		#print("SELECT * FROM " + database + " WHERE email = ':email' AND password = ':password'", {"email": email, "password": password})
		self.cursor.execute("SELECT * FROM " + database + " WHERE email = ':email' AND password = ':password'", {"email": email, "password": password})
		names = self.cursor.fetchall()
		print(names)
		if names == []:
			return False
		else:
			return True

	def createAccount(self, c):
		compressed_data = c.recv(1024)
		data = pickle.loads(compressed_data)
		typeOfUser = data[0]
		name = data[1]
		lastname = data[2]
		email = data[3]
		password = data[4]
		phonenumber = data[5]
		zipCode = data[6]
		self.addUser(typeOfUser, name, lastname, email, password, phonenumber, zipCode)

	def addUser(self, typeOfUser, name, lastname, email, password, phonenumber, zipCode):
		database = "User_Info" if typeOfUser == "Client" else "Seller_Info"
		#print("add : type = %s, email = %s, password = %s" % (typeOfUser, email, password))
		if database == "User_Info":
			self.cursor.execute("INSERT INTO " + database + " VALUES (:name, :lastname, :email, :password, :phonenumber, :zipCode)", {"name": name, "lastname":lastname, "email":email, "password": password, "phonenumber":phonenumber, "zipCode": zipCode})
			print("User added")
		else:
			self.cursor.execute("INSERT INTO " + database + " VALUES (:name, :lastname, :email, :password, :phonenumber, :zipCode, :stock, :price, :openingHours)", {"name": name, "lastname":lastname, "email":email, "password": password, "phonenumber":phonenumber, "zipCode": zipCode, "stock":None, "price": None, "openingHours": None})
			print("Seller added")



if __name__ == "__main__":
	try:
		server = Server()
	except KeyboardInterrupt:
		print("Goodbye :)")