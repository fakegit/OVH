# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 23:12:28 2016

@author: alexis
"""
import socket
import threading

ips = "ip.txt"
noms = "noms.txt"
ports = "ports.txt"
ip_serveur = "127.0.0.1"
port_serveur = 9999
n_co = 1
class ip:
    def __init__(self,name,access_ip,access_port,used=False):
        self.name = name
        self.access_ip = access_ip
        self.access_port = access_port
        self.used = used
        
#on suppose que les listes sont de tailles égales
#a completer
liste_ip = []
liste_port = []
liste_nom = []
#reste vide
liste_objet = []
def import_data(fichier,liste):
    with open(fichier,"r") as fichier:
        for ligne in fichier:
            liste.append(ligne.strip())


def construction_table():
    import_data(ips,liste_ip)
    import_data(noms,liste_nom)
    import_data(ports,liste_port)
    
    for i in range(0,len(liste_ip)):
        liste_objet.append(ip(liste_nom[i],liste_ip[i],liste_port[i]))
    return 0

def reception_requete(ip):
    for i in range(0,len(liste_objet)):
        if liste_objet[i].access_ip == ip:
            if liste_objet[i].used:
                raise NameError("ip déja occupee")
            else:
                liste_objet[i].used = True
    return 0
    
def envoi_proxy(ip):
   

    return 0
if __name__ == "__main__":
    
    serveur = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        serveur.bind(ip_serveur,port_serveur)
    except socket.error:
        print("impossible de lier le serveur a l'ip et au port choisi")
    while True:
        serveur.listen(n_co)
        connexion,addresse = serveur.accept()
        ### a completer
    
    