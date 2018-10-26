#!/usr/bin/env python3

import socket
import threading
import time
import sys
import os
import sqlite3
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

#SERVER_IP="51.75.126.222"
SERVER_IP = "0.0.0.0"

SERVER_PORT=10003

class Server:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connections = []


	def __init__(self):
		self.sock.bind(("0.0.0.0", SERVER_PORT))
		self.sock.listen(1)
		self.letGoSQL()

	def handler(self, c, a, username):
		while True:
			try:
				data = c.recv(1024)
			except Exception as e:
				print(e)
				break
			if not data or [c,username] not in self.connections:
				try:
					self.connections.remove([c,username])
					for connection in self.connections:
						connection[0].send(username+b' disconnected\n')
					c.close()
					print(str(a[0]) + ":" + str(a[1]),"("+str(username,"utf-8")+")", "disconnected")
				except Exception as e:
					print(e)
					pass
				finally:
					break
			data=str(data,"utf-8")
			msg=data.split(maxsplit=2)
			if len(msg)==3 and msg[0]=="/msg":
				for connection in self.connections:
					if connection[1]==bytes(msg[1],"utf-8") or connection[1]==username:
						connection[0].send(username+b' (pm): '+bytes(msg[2],"utf-8"))
			elif len(msg)==1 and msg[0] == "/online":
					users = [str(connection[1],"utf-8") for connection in self.connections]
					c.send(bytes("Users connected:\n"+("\n".join(users) if len(users)>0 else "None"),"utf-8"))
			elif len(msg)==2 and msg[0] == "/online":
					users = [str(connection[1],"utf-8") for connection in self.connections]
					c.send(bytes(msg[1]+(" online" if msg[1] in users else " offline"),"utf-8"))
			else:
				for connection in self.connections:
					connection[0].send(username+b': '+bytes(data,"utf-8"))

	def commandHandler(self):
		while True:
			cmd=input("").split(maxsplit=1)
			if len(cmd)>0:
				if cmd[0]=="msgall" and len(cmd)>1:
					for connection in self.connections:
						connection[0].send(b'[SERVER]: '+bytes(cmd[1],"utf-8"))
				elif cmd[0]=="msg" and len(cmd)>1:
					msg=cmd[1].split(maxsplit=1)
					if len(msg)>1:
						for connection in self.connections:
							if connection[1]==bytes(msg[0],"utf-8"):
								connection[0].send(b'[SERVER (pm)]: '+bytes(msg[1],"utf-8"))
				elif cmd[0]=="kick" and len(cmd)>1:
					closeCons=[]
					for connection in self.connections:
						if str(connection[1],"utf-8") in cmd[1].split():
							closeCons.append(connection)
							connection[0].send(b"You have been kicked ! Press enter to continue.")
					for closeCon in closeCons:
						print(str(closeCon[1],"utf-8")+" kicked")
						for connection in self.connections:
							if connection[0] not in cmd[1].split():
								connection[0].send(closeCon[1]+b' kicked\n')
						self.connections.remove(closeCon)
						closeCon[0].close()
				elif cmd[0]=="online":
					print("Users online:")
					for connection in self.connections:
						print(str(connection[1],"utf-8"))
				elif cmd[0]=="reboot":
					for connection in self.connections:
						connection[0].send(b'[SERVER]: Server will reboot in '+bytes(i)+b"\n")

	def run(self):
		cmdThread = threading.Thread(target=self.commandHandler)
		cmdThread.daemon = True
		cmdThread.start()
		while True:
			c, a = self.sock.accept()
			
			username = c.recv(1024)
			password = c.recv(1024)

			if self.addUser(str(username, "utf-8"), a[0]):
				print(str(a[0]) + ":" + str(a[1]),"("+str(username,"utf-8")+")", "vient de se connecter")
				for connection in self.connections:
					connection[0].send(username+b' vient de se connecter')
				users=[str(connection[1],"utf-8") for connection in self.connections]
				c.send(b"Bienvenue chez Agreez\n")
				c.send(bytes("Utilisateur connecté:\n"+("\n".join(users) if len(users)>0 else "None"),"utf-8"))
				self.connections.append([c,username])
				cThread = threading.Thread(target=self.handler, args=(c, a, username))
				cThread.daemon = True
				cThread.start()
			else:
				print("Cet utilisateur existe deja")
				self.sock.send(b"Sorry this username already exists!")

	def letGoSQL(self):
		self.conn = sqlite3.connect(":memory:")
		self.cursor = self.conn.cursor()
		try:
			self.cursor.execute("""CREATE TABLE User_Info (
					name text,
					lastname text,
					email text,
					password text,
					phonenumber text
					)""")

			print("Database User_Info créée")
		#except sqlite3.OperationalError:
		except Exception :
			print("La database User_Info est déjà crée")
			
		try:
			self.cursor.execute("""CREATE TABLE Seller_Info (
					name text,
					lastname text,
					password text,
					email text,
					phonenumber text,
					stock int,
					price real,
					adress text,
					openingHours text
					)""")
			print("Database Seller_Info créée")
		except Exception:
			print("La database Seller_Info est déjà crée")


	def addUser(self, name, ip)->bool:
		if self.checkIfOk(name):
			with self.conn:
				self.cursor.execute("INSERT INTO User_Info VALUES (:name, :ip)", {'name': name, 'ip': ip})
			print("Utilisateur '{} ({})' ajouté".format(name, ip))
			return True
		else:
			print("L'utilisateur '{} ({})' existe déjà!".format(name, ip))
			return False

	def checkIfOk(self, name)->bool:
		self.cursor.execute("SELECT * FROM User_Info WHERE name = :name", {'name': name})
		names = self.cursor.fetchall()
		if names == []:
			return True
		else:
			return False



if __name__=="__main__":
	try:
		server = Server()
		server.run()
	except Exception as e:
		print(e)
