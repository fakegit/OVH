# -*- encoding: utf-8 -*-
import ovh
import sys
import subprocess
import os
import random

'''
###############################################################
#                                                             #
#                    VARIABLES STATIQUES                      #
#															  #
###############################################################
'''
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"															#Pour la creation de l'identifiant des profils
mozillaPath = "/root/.mozilla"
iniPath = "./partToModify.ini"
prefPath = mozillaPath + "/firefox/templateProfile/prefs.js"
hostname = subprocess.Popen(["hostname"],stdout=subprocess.PIPE).communicate()[0].decode().split('\n')[0]
nbOfInstances = 12

'''
###############################################################
#                                                             #
#              CONFIGURATION DES PROFILS FF                   #
#                                                             #
###############################################################
'''

'''Cree les informations de configuration'''

profiles = {}

for i in range(nbOfInstances):
	index = ""
	for j in range(8):
		index = index + alphabet[random.randrange(0,len(alphabet),1)]
	profiles[i] = {}
	profiles[i]["index"] = index
	profiles[i]["number"] = str(i)
	profiles[i]["name"] = "firefox" + str(i)

'''Copies des templates de profils'''
for i in range(len(profiles)):
	os.system("cp " + mozillaPath + "/firefox/templateProfile -R " + mozillaPath + "/firefox/" + profiles[i]["index"] + "." + profiles[i]["name"])


'''Lire le .ini'''
with open(iniPath,'r') as iF:
	iniConfig = iF.read()

'''Generer les profiles dans le .ini'''

iniProfile = []
for i in range(len(profiles)):
	tempProfile = iniConfig.format(str(i),profiles[i]["name"],profiles[i]["index"])
	iniProfile.append(tempProfile)

'''Lecture du pref.js'''
with open(prefPath,"r") as pF:
	prefConfig = pF.read()

'''Creation des pref.js suivant les profils'''

for i in range(len(profiles)):
	profiles[i]["pref"] = prefConfig.replace("INDEX_PROFILE",profiles[i]["index"]).replace("NAME_PROFILE",profiles[i]["name"]).replace("HOSTNAME",hostname)

'''Edition des pref.js de chaque profil'''

for i in range(len(profiles)):
	with open(mozillaPath + "/firefox/" + profiles[i]["index"] + "." + profiles[i]["name"] + "/prefs.js","w") as pW:
		pW.write(profiles[i]["pref"])

'''Edition du fichier .ini'''
with open(mozillaPath + "/firefox/profiles.ini","w") as iW:
	for i in iniProfile:
		iW.write(i)
