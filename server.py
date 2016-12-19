# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 23:12:28 2016

@author: alexis
"""

class ip:
    def __init__(self,name,access_ip,access_port,used):
        self.name = name
        self.acces_ip = access_ip
        self.access_port = access_port
        self.used = used
        
#on suppose que les listes sont de tailles égales
#a completer
liste_ip = []
liste_port = []
liste_nom = []
#reste vide
liste_objet = []

def construction_table():
    for i in range(0,len(liste_ip)):
        liste_objet.append(ip(liste_nom[i],liste_ip[i],liste_port[i],0))

    
if __name__ == "__main__":
    liste_ip = [1,2,3,4,5]
    liste_port = [1,2,3,4,5]
    liste_nom = [1,2,3,4,5]

    construction_table()
    print(liste_objet)