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
prefPath = "./prefToModify.js"
hostname = sys.argv[1] 	#String 'vps*.ovh.net'
client = ovh.Client() 																						#Ovh.conf
result = client.get('/vps/' + hostname + '/ips') 															#Retourne une liste d'IP du serveur de proxy

'''
###############################################################
#                                                             #
#              CONFIGURATION DES PROFILS FF                   #
#                                                             #
###############################################################
'''

'''Recupere toutes les informations des adresses IPs'''

infos = {}

for i in result:
	infos[i] = client.get('/vps/' + hostname + '/ips/' + i)

'''Trie les IPs selon leur type '''

secondary = []
primary = []

for i in infos:
	if infos[i]["type"] == "primary":
		primary.append(i)
	elif infos[i]["type"] == "additional":
		secondary.append(i)
		
'''Obtenir l'ip principale'''

principal = ""

for i in primary:
	if infos[i]["version"] == 'v4':
		principal = i
		

'''Cree les informations de configuration'''

profiles = {}

for i in range(len(secondary)):
	index = ""
	for j in range(8):
		index = index + alphabet[random.randrange(0,len(alphabet),1)]
	profiles[i] = {}
	profiles[i]["index"] = index
	profiles[i]["number"] = str(i)
	profiles[i]["name"] = "firefox" + str(i)
	profiles[i]["port"] = str(3128 + i)
	profiles[i]["address"] = principal

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

'''Lecture du pref.js'''
with open(prefPath,"r") as pF:
	prefConfig = pF.read()
	
'''Creation des pref.js suivant les profils'''

for i in range(len(profiles)):
	profiles[i]["pref"] = prefConfig.format(profiles[i]["address"],profiles[i]["port"])

'''Edition des pref.js de chaque profil'''

for i in range(len(profiles)):
	with open(mozillaPath + "/firefox/" + profiles[i]["index"] + "." + profiles[i]["name"] + "/prefs.js","a") as pW:
		pW.write(profiles[i]["pref"])
		
'''Edition du fichier .ini'''
with open(mozillaPath + "/firefox/profiles.ini","a") as iW:
	for i in iniProfile:
		iW.write(i)

