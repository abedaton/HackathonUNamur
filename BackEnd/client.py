#!/usr/bin/env python3

import socket
import threading
import time
import sys
import os
import sqlite3
import getpass
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

SERVER_IP = "0.0.0.0"
SERVER_PORT = 10002

class Client:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def __init__(self, address):
		print("plop")
		self.sock.connect((address, SERVER_PORT))

		self.sendInfo()

	def sendInfo(self):
		answer = -1
		print("Etes vous:")
		print("Un Client (1)?")
		print("Un Vendeur(2)?")
		answer = input("1/2 ?")
		print(answer)
		while not (answer == "1" or answer == "2"):
			print("Veuillez entrer 1 ou 2")
			answer = input("1/2 ?")
		print("Bienvenue cher %s" % ("client" if answer == "1" else "vendeur"))
		self.sock.send(b"%s" % b"client" if answer == "1" else b"vendeur")	


if __name__ == "__main__":
	try:
		print("hey")
		client = Client(SERVER_IP)
	except Exception as e:
		print(e)
		print("Goodbye :)")