import time
import ovh
import os

while True:

    time.sleep(3600)

    task = client.post("/vps/vps330953.ovh.net/reboot")

	print("Attente de la fin du redemarrage")

	while int(task['progress']) < 50:
		precPour = task['progress']
		task = client.get("/vps/vps330953.ovh.net/tasks/" + str(task['id']))
		if precPour != task['progress']:
			print("Pourcentage : {} %".format(task['progress']))
		time.sleep(3)
    print("Redemarrage du second serveur")
    task = client.post("/vps/vps338454.ovh.net/reboot")

	print("Attente de la fin du redemarrage")

	while task['state'] != 'done':
		precPour = task['progress']
		task = client.get("/vps/vps338454.ovh.net/tasks/" + str(task['id']))
		if precPour != task['progress']:
			print("Pourcentage : {} %".format(task['progress']))
		time.sleep(3)
