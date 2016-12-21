'''
Ce script va recevoir des requetes en provenance du serveur de controle et transmettra sous une forme representative de
plusieurs objet (tel un json) chaque IPs de proxy associé a ses informatiosn de connexion (IP:PORT)
'''

import cgitb
import json
cgitb.enable(format="text")

with open('proxy.txt','r') as r:
    listProxy = r.read()

listProxyLines = listProxy.split("\n")

DICT_Proxy = {}

for i in listProxyLines:
    DICT_Proxy[listProxyLines.split()[0]] = {}
    DICT_Proxy[listProxyLines.split()[0]]["host"] = listProxyLines.split()[1].split(":")[0]
    DICT_Proxy[listProxyLines.split()[0]]["port"] = listProxyLines.split()[1].split(":")[1]
    DICT_Proxy[listProxyLines.split()[0]]["usedBy"] = ""

STRING_dict_proxy = json.dumps(DICT_Proxy)

print('Content-type: application/json')
print('Content-Disposition: attachment; filename=proxy.json\n')
print(STRING_dict_proxy)
