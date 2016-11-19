#!/usr/bin/python
# -*- encoding: utf-8 -*-
import ovh
import subprocess
import os
requestHostname = subprocess.Popen(["hostname"],stdout=subprocess.PIPE).communicate()[0].decode().split('\n')[0]
client = ovh.Client()
result = client.get('/vps/' + requestHostname + '/ips')
getIPS = {}
for i in range(len(result)):
	getIPS[i] = result[i]
defaultPort = 3128
for i in result:
	if client.get('/vps/' + requestHostname + '/ips/' + i)["type"] == 'primary' and client.get('/vps/' + requestHostname + '/ips/' + i)["version"] == 'v4':
		file = open('/etc/network/interfaces','w')
		defaultConf = open('./defaultConf.conf','r')
		temp = defaultConf.read().format(i)
		file.write(temp)
		defaultConf.close()
		file.close()
		break
precI = []
precA = []
file = open('/etc/network/interfaces',"r")
read = file.read().split('\n')
file.close()
for i in range(len(read)):
	if read[i].split("0")[0] == "iface eth":
		precI.append(read[i])
		if read[i + 1][8] == "a":
			precA.append(read[i + 1].split(' ')[9])
appendice = []
for i in range(len(result)):
	appendice.append("")
	if len(result[i]) <= 15:
		for j in precA:
			if result[i] == j:
				appendice[i] = ""
			else:
				none = ""
				for z in range(17):
					try:
						none = str(precI.index("iface eth0:" + str(z) + " inet static"))
					except ValueError:
						none = "\nauto eth0:" + str(z) + "\niface eth0:" + str(z) + " inet static"
						precI.append("iface eth0:" + str(z) + " inet static")
						#print(precI)
						break
				if len(none) > 3:
					appendice[i] = none + "\n        address " + result[i] + "\n        netmask 255.255.255.255\n        broadcast " + result[i] + "\n"

file = open("/etc/network/interfaces","a")
for i in appendice:
	file.write(i)
file.close()
os.system("sudo service networking restart")
#Config de Squid
ipv4 = 0
for i in result:
	if len(i) <= 15:
		ipv4 = ipv4 + 1
port = 3128
http_port = ""
acl = ""
http_access = ""
tcp_outgoing_address = ""
for i in result:
	if len(i) <= 15:
		if client.get('/vps/' + requestHostname + '/ips/' + i)["type"] == 'primary' and client.get('/vps/' + requestHostname + '/ips/' + i)["version"] == 'v4':
			for j in range(ipv4 - 1):
				http_port = http_port + "http_port " + i + ":" + str(port) + " name=" + str(port) + "\n"
				port = port + 1
for i in range(defaultPort,port):
	acl = acl + "acl port" + str(i) + " myportname " + str(i) + "\n"
	http_access = http_access + "http_access allow port" + str(i) + "\n"
o = 0
for i in result:
	if len(i) <= 15:
		if client.get('/vps/' + requestHostname + '/ips/' + i)["type"] != 'primary':
			tcp_outgoing_address = tcp_outgoing_address + "tcp_outgoing_address " + i + " port" + str(port + o) + "\n"
			o = o + 1
defaultConfSquid = open("./defaultConfSquid.conf","r")
buffer = defaultConfSquid.read().format(http_port,acl,http_access,tcp_outgoing_address)
defaultConfSquid.close()
squid = open("/etc/squid3/squid.conf","w")
squid.write(buffer)
squid.close()
os.system("sudo service squid3 restart")