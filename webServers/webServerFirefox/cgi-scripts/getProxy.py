#!/usr/bin/python

'''
Chaque profiles firefox va demander a ce serveur son fichier.pac (l'appel est géré dans le pref.js)
Ce script va ensuite encoder l'identifiant UNIQUE du profil firefox qu'il enverra au serveur de controle pour obtenir un fichier.pac convenable
Une fois le fichier .pac reçu , ce script va le renvoyer au profil firefox ce qui lui permettra de se connecter à internet
'''
