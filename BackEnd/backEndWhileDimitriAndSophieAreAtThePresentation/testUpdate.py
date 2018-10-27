import sqlite3
import pickle

conn = sqlite3.connect(":memory:", check_same_thread = False) # Using :memory: pour le moment, eviter de recréer un fichier .db chaque fois
cursor = conn.cursor()
def goSQL():
	try:
		cursor.execute("""CREATE TABLE User_Info (
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
		cursor.execute("SELECT * FROM User_Info;")
		print(cursor.fetchall())
	
	try:
		cursor.execute("""CREATE TABLE Seller_Info (
			name text,
			lastname text,
			password text,
			email text,
			phonenumber text,
			zipCode bigint,
			item blob,
			stock blob,
			price blob,
			openingHours text
			)""")
		print("Database Seller_Info créée")
	except:
		print("La table Seller_Info existe déjà")
		cursor.execute("SELECT * FROM Seller_Info;")
		print(cursor.fetchall())


def addUpdateItem(item, quantity, price = 0.0):
	cursor.execute("SELECT stock, price FROM Seller_Info")
	liste = cursor.fetchall()
	alll = liste
	if alll == []:
		alll = [[], [], []]
	oldItems = alll[0]
	oldStock = alll[1]
	oldPrice = alll[2]
	if item in oldItems:
		newStock = oldStock + quantity # meme negatif
		dStock = pickle.dumps(newStock)
		dItems = pickle.dumbs(oldItems)
		dPrice = picle.dumps(oldPrice)
	else:
		newItems = oldItems + [item]
		dItems = pickle.dumps(newItems)
		newStock = [quantity]
		dStock = pickle.dumps(newStock)
		newPrice = [price]
		dPrice = pickle.dumps(newPrice)
	print("plop")
	cursor.execute("UPDATE Seller_Info SET (item, stock, price) = (?, ?, ?)", (dItems, dStock, dPrice))
	cursor.execute("SELECT * FROM Seller_Info")
	result = cursor.fetchall()
	print(result)

goSQL()
addUpdateItem("pomme", 6)
conn.execute("SELECT * FROM Seller_Info")
print(cursor.fetchall())