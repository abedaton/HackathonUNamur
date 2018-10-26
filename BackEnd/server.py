#!/usr/bin/env python3

import socket
import threading
import time
import sys
import os
import sqlite3
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


	def run(self):
		while True:
			c, a = self.sock.accept()
			typeOfUser = c.recv(1024)
			print("typeOfUser = ", typeOfUser)
			action = c.recv(1024)
			print("action = ", action)


if __name__ == "__main__":
	try:
		print("plop")
		server = Server()
		server.run()
	except KeyboardInterrupt:
		print("Goodbye :)")