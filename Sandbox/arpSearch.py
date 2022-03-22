import time
import socket
import storage
import subprocess

def arpsearch ():

	search = 1

	while True:

		if (storage.exit):

			break

		#with open("logARP.txt", 'a') as f:

		#	f.write(f"Starting Search {search}\n\n")

		hostsAndIPs = subprocess.run(["arp", "-a"], capture_output = True).stdout.decode("UTF-8")

		split = hostsAndIPs.split("\n")

		for i in range(len(split)):

			split[i] = split[i].split(" ")

		for i in split:

			if (len(i) == 1):

				continue

			ip = i[1][1:-1]

			ips = [storage.devicesARP[x][0] for x in range(len(storage.devicesARP))]

			if not(ip in ips):

				if (i[0] == "?"):

					try:

						host = socket.gethostbyaddr(ip)

						storage.devicesARP.append([ip, host])

					except Exception as e:

						storage.devicesARP.append([ip, i[0]])

				else:

					storage.devicesARP.append([ip, i[0]])

				with open("logARP.txt", 'a') as f:

					f.write(f"Adding ARP host with name {i[0]} and ip of {ip} to list\n")

		#with open("logARP.txt", 'a') as f:

		#	f.write(f"\n")

		#with open("logARP.txt", 'a') as f:

		#	f.write(f"Updated ARP Hosts: {[storage.devicesARP[x][1] for x in range(len(storage.devicesARP))]}\nHost List has a length of {len(storage.devicesARP)}\n\n")

		search += 1

		time.sleep(1)