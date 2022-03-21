import time
import socket
import struct
import storage
import threading
import netifaces
import ipaddress

def sendToHost (ip):

	try:

		host = socket.gethostbyaddr(ip)

		ips = [storage.devicesIP[x][0] for x in range(len(storage.devicesIP))]
		hostNames = [storage.devicesIP[x][1] for x in range(len(storage.devicesIP))]

		ipsARP = [storage.devicesARP[x][0] for x in range(len(storage.devicesARP))]
		hostNamesARP = [storage.devicesARP[x][1] for x in range(len(storage.devicesARP))]

		if (any(x in ips for x in host[2]) and not(host[0] in hostNames)):

			storage.devicesIP[ips.index(host[2][0])] = [host[2][0], host[0]]

		elif (any(x in ipsARP for x in host[2]) and not(host[0] in hostNamesARP)):

			storage.devicesARP[ipsARP.index(host[2][0])] = [host[2][0], host[0]]

		elif not(host[2][0] in ips):

			with open("logIP.txt", 'a') as f:

				f.write(f"Added IP host with name {host[0]}, ip {host[2][0]}, and alias {host[1]}\n")

			storage.devicesIP.append([host[2][0], host[0]])

		return host[0]

	except Exception as e:

		#with open("logIP.txt", 'a') as f:

		#	f.write(f"\nError: {e}\n\n")

		pass

	return ""

def convertToCIDR (ip, mask):

	maskCIDR = "".join([str(bin(int(x))[2:]) for x in mask.split(".")])

	maskCIDRCount = maskCIDR.count("1")

	return f"{ip}/{maskCIDRCount}"

def scrub (arr):

	temp_array = arr

	for i in range(len(arr) - 1, -1, -1):

		if (temp_array[i] == ""):

			temp_array.pop(i)

	return arr

def clean (arr):

	hostNames = [storage.devicesIP[x][1] for x in range(len(storage.devicesIP))]

	for i in arr:

		if not(i in hostNames):

			storage.devicesIP.pop(hostNames.index(i))
			hostNames = [storage.devicesIP[x][1] for x in range(len(storage.devicesIP))]

def ipsearch ():

	search = 1

	while True:

		if (storage.exit):

			break

		#with open("logIP.txt", 'a') as f:

		#	f.write(f"Starting Search {search}\n\n")

		toBeSearched = []

		for i in netifaces.ifaddresses('en0')[netifaces.AF_INET]:

			toBeSearched.append(ipaddress.IPv4Network(convertToCIDR(i['addr'], i['netmask']), strict = False))

		#with open("logIP.txt", 'a') as f:

		#	f.write(f"Ip Ranges: {toBeSearched}\n\n")

		updated = []

		for i in toBeSearched:

			for j in i:

				updated.append(findHost(str(j)))

		clean(scrub(updated))

		#with open("logIP.txt", 'a') as f:

		#	f.write(f"Updated IP Hosts: {[storage.devicesIP[x][1] for x in range(len(storage.devicesIP))]}\nHost List has a length of {len(storage.devicesIP)}\n\n")

		search += 1

		time.sleep(1)

	with open("logIP.txt", 'a') as f:

		f.write(f"Done\n\n")
