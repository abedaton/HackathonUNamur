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
		self.conn = sqlite3.connect(":memory:") # Using :memory: pour le moment, eviter de recréer un fichier .db chaque fois
		self.cursor = self.conn.cursor()

		try:
			self.cursor.execute("""CREATE TABLE User_Info (
				name text,
				lastname text,
				email text,
				password text,
				phonenumer text
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
				stock bigint,
				price real,
				zipCode bigint,
				openingHours text
				)""")
			print("Database Seller_Info créée")
		except:
			print("La table Seller_Info existe déjà")


	def getConnection(self):
		while True:
			c, a = self.sock.accept()
			print(str(a[0]) + ":" + str(a[1]) + " vient de se connecter")
			c.send(b"Bienvenue chez Agreez\n")
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
		print(data)


if __name__ == "__main__":
	try:
		server = Server()
	except KeyboardInterrupt:
		print("Goodbye :)")