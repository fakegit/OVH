#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
Dans l'autre cas , ce script va lire une base de donnée contenant des representations objectives de proxy (tel un json)
va les interpreter et renverra sous la forme d'un fichier .pac le premier proxy libre qu'elle trouvera
'''

import cgi
import cgitb
import json
import urllib
import os

cgitb.enable(format='text')

'''Cette fonction permet d'aléger le code présent dans le serveur firefox en permettant de formater le dictionnaire de maniere préétablie avec l'identifiant comme ceci:

{
    "IDENT_FIREFOX": {
        "host": "PROXY_VPS_PRINCIPAL_IP",
        "port": PROXY_VPS_PORT_SQUID3
    }
}
'''


def extractContentFromProxy(proxy_list,ident,proxy_to_use):
    new_json = {}
    new_json[ident] = {}
    new_json[ident]["host"] = proxy_list[str(proxy_to_use)]["host"]
    new_json[ident]["port"] = proxy_list[str(proxy_to_use)]["port"]
    return new_json


print('Content-type: application/json')
print('Content-Disposition: attachment; filename=proxy.json\n')

'''Ici , nous recuperrons l'identifiant firefox donné en argument'''

formulaire = cgi.FieldStorage()
ident = cgi.escape(formulaire.getvalue("ident"))

'''Ici , nous recuperons une liste de proxy sous la forme :


{
    "PROXY_IP" : {
        host: "PROXY_VPS_PRINCIPAL_IP",
        port: PROXY_VPS_PORT_SQUID3
        usedBy: ""
    }, ...
}
'''

try:
    with open("proxy_list.json","r") as r:
        proxy_list = r.read()
except:
    proxy_json = urllib.urlretrieve("http://vps338300.ovh.net/cgi-scripts/getAllProxys.py", filename="temp.json")
    with open("temp.json","r") as r:
        proxy_list = r.read()
    os.system('rm temp.json')

'''Nous transformons la chaine en dictionnaire'''

DICT_proxy_list = json.loads(proxy_list)
proxy_to_use = ""
for i in DICT_proxy_list:
    if DICT_proxy_list[i]["usedBy"] == "":
        proxy_to_use = i
    elif DICT_proxy_list[i]["usedBy"] == ident:
        proxy_to_use = i
        break
if proxy_to_use != "":
    json_to_send = extractContentFromProxy(DICT_proxy_list,ident,proxy_to_use)
    DICT_proxy_list[proxy_to_use]["usedBy"] = ident
else:
    json_to_send = {str(ident): {"host": "127.0.0.1","port": "8080"}}

STRING_proxy_list = json.dumps(DICT_proxy_list)

with open("proxy_list.json","w") as w:
    w.write(STRING_proxy_list)

'''Puis nous les envoyons '''

print(json.dumps(json_to_send))
