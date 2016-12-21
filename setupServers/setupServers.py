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
mode = sys.argv[2]																							#proxy/firefox : Mode de reinstallation
sshK = "ssh-key"																							#Clé standard SSH
defaultLanguage = "en"																						#Language standard anglais
hostname = subprocess.Popen(["hostname"],stdout=subprocess.PIPE).communicate()[0].decode().split('\n')[0]
client = ovh.Client()																						#Ovh.conf
ipList = client.get('/vps/' + vps + '/ips')																	#Liste d'IP du serveur cible

try:																										#Options de reinstallations
	options = sys.argv[3]																					#11 : Total
except IndexError:																							#10 : Reinstallation
	options = "11"																							#01 : Configuration seulement


'''
###############################################################
#                                                             #
#               VERIFICATION DES INFOS BASE                   #
#                                                             #
###############################################################
'''
if mode != "proxy" and mode != "firefox":
	SystemExit("Le mode de reinstallation specifie est incorrect")

'''
###############################################################
#                                                             #
#                REINSTALLATION DU SERVICE                    #
#                                                             #
###############################################################
'''
if options[0] == "1":

	'''Recuperation de l'adresse IPv4 du serveur cible'''

	print("Recuperation de l'adresse IPv4 du serveur cible")

	infosIP = {}

	for i in ipList:
		infosIP[i] = client.get('/vps/' + vps + '/ips/' + i)

	ipv4 = ""																									#Adresse IPV4 du serveur

	for i in infosIP:
		if infosIP[i]["type"] == "primary" and infosIP[i]["version"] == "v4":
			ipv4 = i

	'''Suppression du vps de la liste des hotes connus'''

	print("Suppression du vps de la liste des hotes connus")

	os.system('ssh-keygen -f "/root/.ssh/known_hosts" -R {}'.format(vps))										#Suppression du nom d'hote
	os.system('ssh-keygen -f "/root/.ssh/known_hosts" -R {}'.format(ipv4))										#Suppression de l'adresse IP

	'''Recuperation du template de Debian 8'''

	print("Suppression du vps de la liste des hotes connus")

	templates = client.get("/vps/" + vps + "/templates")

	infosTemplates = {}

	for i in templates:
		infosTemplates[i] = client.get("/vps/" + vps + "/templates/" + str(i))

	templateID = 0

	for i in infosTemplates:
		if infosTemplates[i]["distribution"] == "debian8":
			templateID = i

	'''Reinstallation avec les parametres de configuration'''

	print("Reinstallation avec les parametres de configuration")

	task = client.post("/vps/" + vps + "/reinstall",doNotSendPassword=False,language="en",sshKey=["ssh-key"],templateId=templateID)

	'''Attente de la fin de la reinstallation'''

	print("Attente de la fin de la reinstallation")

	while task['state'] != 'done':
		precPour = task['progress']
		task = client.get("/vps/" + vps + "/tasks/" + str(task['id']))
		if precPour != task['progress']:
			print("Pourcentage : {} %".format(task['progress']))
		time.sleep(3)
else:
	print("Skipping reinstallation")

'''
###############################################################
#                                                             #
#                 CONFIGURATION DU SERVICE                    #
#                                                             #
###############################################################
'''
if options[1] == "1":
	'''Recuperation des commandes'''

	print("Recuperation des commandes")
	commands = ""

	if mode == "firefox":
		commandPath = "/root/OVH/setupFirefoxServer/commands"
		domain = sys.argv[4]
	elif mode == "proxy":
		commandPath = "/root/OVH/setupProxyServer/commands"

	with open(commandPath,'r') as r:
		commands = r.read()

	'''Separation des nouvelles lignes (une commande par ligne) + formatage avec l'ip'''

	print("Separation des nouvelles lignes (une commande par ligne) + formatage avec l'ip")

	commandsList = []

	for i in commands.split('\n'):
		if mode == "firefox":
			commandLine = i.format(vps,domain)
		elif mode == "proxy":
			commandLine = i.format(vps)
		commandsList.append(commandLine)

	'''Envoi des commandes ssh multiples'''

	print("Envoi des commandes ssh multiples")

	for i in commandsList:
		print("Sending :",i)
		os.system(i)

	os.system("python ../webServers/setServer.py " + str(vps) + " " + str(mode))

else:
	print("Skipping configuration")
