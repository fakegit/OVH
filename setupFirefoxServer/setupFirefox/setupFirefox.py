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
iMS = ["mkdir /etc/service/firefox{0}","cp /root/setupFirefox/run /etc/service/firefox{0}"]
iMS_A = ["chmod 755 /etc/service/firefox{0}/run","chmod 1755 /etc/service/firefox{0}"]
script = "#!/bin/sh\nDISPLAY=:1 exec firefox -P firefox{0} -no-remote imacros://run/?m=autosurf.iim"
nbOfInstances = 6

'''
###############################################################
#                                                             #
#              CONFIGURATION DES PROFILS FF                   #
#                                                             #
###############################################################
'''

'''IMACROS TEST'''

os.system('/etc/rc.local csh -cf \'svscanboot &\'')
os.system('sed -i "1 a\csh -cf \'svscanboot &\'" /etc/rc.local')
os.system('chmod +x /etc/')
os.system('mkdir /etc/service')

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


'''Imacros Stuff'''
for i in range(nbOfInstances):
	for j in iMS:
		os.system(j.format(str(i)))
	with open("/etc/service/firefox{0}/run".format(str(i)),"w") as w:
		w.write(script.format(i))
	for j in iMS_A:
		os.system(j.format(str(i)))
