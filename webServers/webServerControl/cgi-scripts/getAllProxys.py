#!/usr/bin/python
# -*- encoding: utf-8 -

import cgi
import cgitb
import json
import urllib
cgitb.enable(format='text')

def concatDict(dict1,dict2):
    dict3 = {}
    for i in dict1:
        dict3[i] = dict1[i]
    for i in dict2:
        dict3[i] = dict2[i]
    return dict3

proxy_vps_list = ["137.74.195.38"] '''A REFAAAAAAAAAAAAAAAAAAAAAAAAIIIIIIIIIIIIIIIIIIIIIIIIIRRRRRRRRRRRRRRRRRRRRRREEEEEEEEEEEEEEEEEEEEE'''

proxys = {}

for i in range(len(proxy_vps_list)):
    proxy_json = urllib.urlretrieve("http://" + proxy_vps_list[i] + "/cgi-scripts/getIP.py" , filename="temp.json")
    with open("temp.json","r") as r:
        tempProxy = r.read()
    proxys = concatDict(proxys,json.loads(tempProxy))
    os.system("rm temp.json")

print('Content-type: application/json')
print('Content-Disposition: attachment; filename=proxy.json\n')

print(json.dumps(proxys))
