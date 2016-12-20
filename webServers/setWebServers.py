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
        os.system(i.format(vps,"Firefox"))
elif mode == "proxy":
    for i in commandList.split("\n"):
        os.system(i.format(vps,"Proxy"))
