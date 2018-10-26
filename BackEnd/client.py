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
		self.sock.connect((address, SERVER_PORT))

		self.sendInfo()

	def sendInfo(self):
		answer = -1
		print("Etes vous:")
		print("Un Client (1)?")
		print("Un Vendeur(2)?")
		answer = input("1/2 ? ")
		print(answer)
		while not (answer == "1" or answer == "2"):
			print("\nVeuillez entrer 1 ou 2")
			answer = input("1/2 ? ")
		print("Bienvenue cher %s" % ("client" if answer == "1" else "vendeur"))
		self.sock.send(b"%s" % b"client" if answer == "1" else b"vendeur")	
		typeOfUser = "Client" if answer == "1" else "Vendeur"
		print("Voulez-vous:")
		print("Se connecter(1)?")
		print("Creer un compte(2)?")
		newAnswer = input("1/2 ? ")
		while not (newAnswer == "1" or newAnswer == "2"):
			print("\nVeuillez choisir entre 1 ou 2")
			newAnswer = input("1/2 ? ")
		self.sock.send(b"%s" % b"connection" if newAnswer == "1" else b"Create")
		[self.connection(typeOfUser) if newAnswer == "1" else self.createAccount(typeOfUser)]






	def connection(self, typeOfUser):
		email = input("Address email: ")
		password = getpass.getpass() # pour ne pas voir le mot de passe s'afficher


	def createAccount(self, typeOfUser):
		pass

if __name__ == "__main__":
	try:
		client = Client(SERVER_IP)
	except Exception as e:
		print(e)
		print("Goodbye :)")