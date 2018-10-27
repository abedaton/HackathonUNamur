#!/usr/bin/env python3

import socket
import threading
import time
import sys
import os
import sqlite3
import pickle
from signal import signal, SIGPIPE, SIG_DFL
import smtplib 
import hashlib
import array
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
		self.conn = sqlite3.connect("../database.db", check_same_thread = False) # Using :memory: pour le moment, eviter de recréer un fichier .db chaque fois
		self.cursor = self.conn.cursor()

		try:
			self.cursor.execute("""CREATE TABLE User_Info (
				name text,
				lastname text,
				password text,
				email text,
				phonenumber text,
				zipCode bigint
				)""")
			print("Database User_Info créée")
		except:
			print("La table User_Info existe déjà")
			self.cursor.execute("SELECT * FROM User_Info;")
			print(self.cursor.fetchall())
		
		try:
			self.cursor.execute("""CREATE TABLE Seller_Info (
				name text,
				lastname text,
				password text,
				email text,
				phonenumber text,
				zipCode bigint,
				stock blob,
				price blob,
				openingHours text
				)""")
			print("Database Seller_Info créée")
		except:
			print("La table Seller_Info existe déjà")
			self.cursor.execute("SELECT * FROM Seller_Info;")
			print(self.cursor.fetchall())


	def getConnection(self):
		while True:
			self.c, a = self.sock.accept()
			print(str(a[0]) + ":" + str(a[1]) + " vient de se connecter")
			self.connections.append(self.c)
			clientThread = threading.Thread(target=self.handleEachUser)
			clientThread.daemon = True
			clientThread.start()


	def handleEachUser(self):
		typeOfUser = self.c.recv(1024) 
		action = self.c.recv(1024)
		[self.login() if action == b"connection" else self.createAccount()]

	def login(self):
		compressed_data = self.c.recv(1024)
		data = pickle.loads(compressed_data)
		typeOfUser = data[0]
		email = data[1]
		password = self.letsHash(data[2])
		if self.checkOK(typeOfUser, email, password):
			self.c.send(b"User logged in as " + bytes(email, "utf-8"))
		else:
			self.c.send(b"Wrong Username or password!")

	def checkOK(self, typeOfUser, email, password):
		database = "User_Info" if typeOfUser == "Client" else "Seller_Info"
		print("check : database = %s, email = %s, password = %s" % (database, email, password))
		
		self.cursor.execute("SELECT * FROM " + database + " WHERE email = :email AND password = :password;", {"email": email, "password":password})
		names = self.cursor.fetchall()
		print(names)
		if names == []:
			return False
		else:
			return True

	def createAccount(self):
		compressed_data = self.c.recv(1024)
		data = pickle.loads(compressed_data)
		print(data)
		typeOfUser = data[0]
		name = data[1]
		lastname = data[2]
		email = data[3]
		password = self.letsHash(data[4])
		phonenumber = data[5]
		zipCode = data[6]
		self.addUser(typeOfUser, name, lastname, email, password, phonenumber, zipCode)

	def addUser(self, typeOfUser, name, lastname, email, password, phonenumber, zipCode):
		database = "User_Info" if typeOfUser == "Client" else "Seller_Info"
		if database == "User_Info":
			self.cursor.execute("INSERT INTO User_Info(name, lastname, email, password, phonenumber, zipCode) VALUES (?, ?, ?, ?, ?, ?)", (name, lastname, email, password, phonenumber, zipCode))
			self.conn.commit()
			print("User added")
		else:
			self.cursor.execute("INSERT INTO Seller_Info(name, lastname, email, password, phonenumber, zipCode) VALUES (?, ?, ?, ?, ?, ?)", (name, lastname, email, password, phonenumber, zipCode))
			self.conn .commit()
			print("Seller added")
		self.c.send(b"Vous avez ete inscrit!")

	def letsHash(self, password):
		for i in range(1000):
			password = hashlib.md5(bytes(password, "utf-8")).hexdigest()
		return password

	#def addUpdateItem(self, item, quantity):
	#	self.cursor.execute()
	#	oldItem = 
	#	self.cursor.execute("UPDATE Seller_Info SET")


if __name__ == "__main__":
	try:
		server = Server()
	except KeyboardInterrupt:
		print("Goodbye :)")


