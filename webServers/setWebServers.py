# -*- encoding: utf-8 -*-
import sys
import ovh
import subprocess
import os
import time

'''
###############################################################
#                                                             #
#                    VARIABLES STATIQUES                      #
#															  #
###############################################################
'''

vps = sys.argv[1]																							#Nom du vps a configurer
mode = sys.argv[2]


'''
###############################################################
#                                                             #
#              REINSTALLATION DU WEBSERVER                    #
#                                                             #
###############################################################
'''

with open("commands","r") as r:
    commandList = r.read()

if mode == "firefox":
    for i in commandList.split("\n"):
        print("Sending :",i.format(vps,"Proxy"))
        os.system(i.format(vps,"Firefox"))
elif mode == "proxy":
    commandList = commandList + "\n" + '"mv /root/setupProxy/proxy.txt ../webServer/cgi-scripts/proxy.txt"'
    for i in commandList.split("\n"):
        print("Sending :",i.format(vps,"Proxy"))
        os.system(i.format(vps,"Proxy"))
