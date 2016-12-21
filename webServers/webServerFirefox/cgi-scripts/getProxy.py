#!/usr/bin/python
# -*- encoding: utf-8 -*-

'''
Chaque profiles firefox va demander a ce serveur son fichier.pac (l'appel est gere dans le pref.js)
Ce script va ensuite encoder l'identifiant UNIQUE du profil firefox qu'il enverra au serveur de controle pour obtenir un fichier.pac convenable
Une fois le fichier .pac recu , ce script va le renvoyer au profil firefox ce qui lui permettra de se connecter a internet
'''

import cgi
import cgitb
import json
import urllib


print('Content-type: application/x-ns-proxy-autoconfig')
print('Content-Disposition: attachment; filename=proxy.pac\n')

cgitb.enable(format='text')
formulaire = cgi.FieldStorage()
ident = cgi.escape(formulaire.getvalue("ident"))

try:
    with open("ident.json" ,"r") as r:
        listOfIdent = r.read()
except:
    listOfIdent = "{}"

DICT_listOfIdent = json.loads(listOfIdent)
HTTP_Proxy = {}

for i in DICT_listOfIdent:
    if i == ident:
        HTTP_Proxy = DICT_listOfIdent[i]

if HTTP_Proxy == {}:
    proxy_json = urllib.urlretrieve("http://vps338300.ovh.net/cgi-scripts/proxypac.py?ident=" + str(ident) , filename="temp.json")

    with open("temp.json","r") as r:
        JSON_tempIdent = r.read()

    DICT_tempIdent = json.loads(JSON_tempIdent)

    DICT_listOfIdent[ident] = DICT_tempIdent[ident]

    HTTP_Proxy = DICT_listOfIdent[ident]

listOfIdent = json.dumps(DICT_listOfIdent)

with open("ident.json","w") as w:
    w.write(listOfIdent)

print('function FindProxyForURL(url, host) {\n')
print('return "PROXY ' + str(HTTP_Proxy["host"]) + ':' + str(HTTP_Proxy["port"]) + '; DIRECT";')
print('}')
