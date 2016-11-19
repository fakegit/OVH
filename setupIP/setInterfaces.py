# -*- encoding: utf-8 -*-
import ovh
import subprocess
import os

'''
###############################################################
#                                                             #
#                    VARIABLES STATIQUES                      #
#															  #
###############################################################
'''

interfacePath = "/etc/network/interfaces"
squidPath = "/etc/squid3/squid.conf"
hostname = subprocess.Popen(["hostname"],stdout=subprocess.PIPE).communicate()[0].decode().split('\n')[0] 	#String 'vps*.ovh.net'
client = ovh.Client() 																						#Ovh.conf
result = client.get('/vps/' + hostname + '/ips') 															#Retourne une liste d'IP

'''
###############################################################
#                                                             #
#              CONFIGURATION DES INTERFACES                   #
#                                                             #
###############################################################
'''

'''Recupere la configuration de base/Ecris la config de base'''

if os.path.exists("./interfaces_backup"):
	with open("./interfaces_backup","r") as r:
		config_backup = r.read()
	with open(interfacePath,"w") as w:
		w.write(config_backup)
else:
	with open(interfacePath,"r") as r:
		config_backup = r.read()
	with open("./interfaces_backup","w") as w:
			w.write(config_backup)

'''Recupere la config non formattée'''

with open('./defaultConf.conf', 'r') as f:
	config = f.read()

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
		
'''Obtenir l'ip principale (pour squid)'''

principal = ""

for i in primary:
	if infos[i]["version"] == 'v4':
		principal = i

'''Numérote les addresses ips additionelles'''

getIPS = {}

for i in range(len(secondary)):
	getIPS[i] = secondary[i]
	
'''Création des configs formattées'''

configs = []

for i in getIPS:
	configs.append(config.format(i,getIPS[i]))
	
with open(interfacePath,"a") as f:
	for i in configs:
		f.write(i)

		
'''
###############################################################
#                                                             #
#                  CONFIGURATION DE SQUID                     #
#                                                             #
###############################################################
'''

'''Recupération de la config statique'''

with open('./defaultConfSquid.conf','r') as dfs:
	config_squid = dfs.read()
	
defaultPort = 3128
	
'''Création des configs non formattées'''
	
http = "http_port " + principal + ":{0} name={0}\n" 	#0: Port
acl = "acl port{0} myportname {0}\n" 					#0: Port
http_access = "http_access allow port{0}\n" 			#0: Port
tcp = "tcp_outgoing_address {0} port{1}\n"  			#0: IP SECONDAIRE , 1:Port

'''Configuration des options squid'''

https = ""
acls = ""
http_accesss = ""
tcps = ""

for i in range(len(secondary)):
	https = https + http.format(defaultPort + i)
	acls = acls + acl.format(defaultPort + i)
	http_accesss = http_accesss + http_access.format(defaultPort + i)
	tcps = tcps + tcp.format(secondary[i],defaultPort + i)

'''Formattage de la configuration'''

new_config_squid = config_squid.format(https,acls,http_accesss,tcps)

'''Ecriture dans le fichier'''

with open(squidPath,'w') as w:
	w.write(new_config_squid)
	
'''
###############################################################
#                                                             #
#                        FINALISATION                         #
#                                                             #
###############################################################
'''

os.system("sudo service networking restart")
os.system("sudo service squid3 restart")
