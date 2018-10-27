#!/usr/bin/env python3

import socket
import threading
import time
import sys
import os
import getpass
import pickle
import re
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
		email = input("\nAddress email: ")
		while not re.match(r"[^@]+@[^@]+\.[^@]+", email):
			print("please enter a valid email address")
			email = input("\nAddress email: ")
		password = getpass.getpass() # pour ne pas voir le mot de passe s'afficher
		data = pickle.dumps([typeOfUser, email, password])
		self.sock.send(data)
		loggedOrNot = self.sock.recv(1024)
		print(str(loggedOrNot, "utf-8"))

	def createAccount(self, typeOfUser):
		email = input("\nAddress email: ")
		while not re.match(r"[^@]+@[^@]+\.[^@]+", email):
			print("please enter a valid email address")
			email = input("\nAddress email: ")
		password = getpass.getpass()
		cpassword = getpass.getpass(prompt="Confirm password: ")
		while password != cpassword:
			print("Les deux passwords ne match pas")
			password = getpass.getpass()
			cpassword = getpass.getpass(prompt="Confirm password: ")
		name = input("Entrez votre prénom: ")
		lastname = input("Entrez votre nom: ")
		while True:
			phonenumer = input("Entrez votre numero de telephone: ")
			if phonenumer.isdigit():
				break
			else:
				print("Veuillez entrer un numero de telephone valide!")
		while True:
			try:
				zipCode = int(input("Veuillez entrer votre code postal: "))
				break
			except:
				print("Veuillez entrer un numero de code postal valide!")
		data = pickle.dumps([typeOfUser, name, lastname, email, password, phonenumer, zipCode])
		self.sock.send(data)
		connectedOrNot = self.sock.recv(1024)
		print(str(connectedOrNot, "utf-8"))






if __name__ == "__main__":
	try:
		client = Client(SERVER_IP)
	except Exception as e:
		print(e)
		print("Goodbye :)")