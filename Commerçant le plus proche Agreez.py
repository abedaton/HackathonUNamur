# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 11:56:01 2018

@author: Sandra
"""
import requests
from bs4 import BeautifulSoup

adresse_client = ("Rue de la bonne reine")
adresse_commercant1 = ("Place Edouard Pinoy")

CONSTANTE_URL_ENDROIT = "https://www.openstreetmap.org/search?query="

def transformation_string(adresse):
    adresse = adresse.replace(" ","%20")
    return adresse
    
def envoi_de_l_adresse(adresse,CONSTANTE):
    Url = CONSTANTE + transformation_string(adresse)
    r = requests.post(Url)
    print(r.url)
    

def iteneraire_commercant(adresse_client,adresse_commercant):
    r = requests.get("https://www.openstreetmap.org/directions")
    html = r.content
    soup = BeautifulSoup(html,"html5lib")
    print(soup.attrs)
        
envoi_de_l_adresse(adresse_client,CONSTANTE_URL_ENDROIT)
