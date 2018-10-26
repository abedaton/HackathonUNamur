import socket
import threading
import time
import sys
import os
import sqlite3
import getpass
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

SERVER_IP = "0.0.0.0"
SERVER_PORT=10002

class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, address):
        self.sock.connect((address, SERVER_PORT))
        
        #self.username = input("Entrez votre pseudo: ")
        self.sendUsername()

        self.iThread = threading.Thread(target = self.sendMsg)
        self.iThread.daemon = True
        self.iThread.start()


        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            msg=str(data,"utf-8")
            color="yellow" if ":" not in msg else "green" if msg[:msg.index(":")] in [self.username,self.username+" (pm)"] else "red" if msg[:7]=="[SERVER" else "cyan"
            if color=="green":
                msg="Message envoyé"
            print(msg)

    def sendUsernameAndPassword(self):
        while True:
            self.username = getpass.getpass()
            if self.username.split() != []:
                self.sock.send(bytes(self.username, "utf-8"))
                answer = self.sock.recv(1024)
                print(str(answer, "utf-8"))
                #if answer != b"Sorry this username is already exists!":
                while True:
                    self.username = input("Entrez votre password: ")
                    if self.username.split() != []:
                        self.sock.send(bytes(self.username, "utf-8"))
                        answer = self.sock.recv(1024)
                        print(str(answer, "utf-8"))    

    def sendMsg(self):
     #   self.sock.send(bytes(self.username, "utf-8"))
        while True:
            msg=input("")
            if len(msg)>0 and msg[0]=="!":
                os.system(msg[1:])
            else:
                self.sock.send(bytes(msg, "utf-8"))

if __name__ == "__main__":
    try:
        client = Client(SERVER_IP)
    except Exception as e:
        print(e)
