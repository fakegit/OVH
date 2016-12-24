#!/usr/bin/python
# -*- encoding: utf-8 -

import cgi
import cgitb
import json
import urllib
import os

cgitb.enable(format='text')

'''Cette fonction permet de concatener deux dictionnaires'''

def concatDict(dict1,dict2):
    dict3 = {}
    for i in dict1:
        dict3[i] = dict1[i]
    for i in dict2:
        dict3[i] = dict2[i]
    return dict3

proxy_vps_list = ["137.74.195.38"]

'''A REFAAAAAAAAAAAAAAAAAAAAAAAAIIIIIIIIIIIIIIIIIIIIIIIIIRRRRRRRRRRRRRRRRRRRRRREEEEEEEEEEEEEEEEEEEEE'''

'''Ici , nous recuperons les proxys sous une forme de dictionnaire'''

proxys = {}

'''Pour chaque vps dénominé proxy , nous lui demandons un retour de sa liste de proxy , que nous concatenons avec la liste deja établie'''

for i in range(len(proxy_vps_list)):
    proxy_json = urllib.urlretrieve("http://" + proxy_vps_list[i] + "/cgi-scripts/getIP.py" , filename="temp.json")
    with open("temp.json","r") as r:
        tempProxy = r.read()
    proxys = concatDict(proxys,json.loads(tempProxy))
    os.system("rm temp.json")

print('Content-type: application/json')
print('Content-Disposition: attachment; filename=proxy.json\n')

'''Ici , les proxys sont envoyés sous la forme d'une chaine de caracteres. Elle a ce format :

{
    "PROXY_IP" : {
        host: "VPS_PRINCIPAL_IP",
        port: PORT_FOR_SQUID3
        usedBy: ""
    }, ...
}
'''

print(json.dumps(proxys, sort_keys=True, indent=4,separators=(',', ': ')))
