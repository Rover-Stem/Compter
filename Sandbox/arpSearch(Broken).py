import time
import socket
import struct
import storage
import logging
import threading
import netifaces
import ipaddress

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import ARP, Ether, srp

def findHost (ip):

	try:

		host = socket.gethostbyaddr(ip)

		with open("log.txt", 'a') as f:

			f.write(f"Found host with name {host[0]}, ip {host[2]}, and alias {host[1]}\n")

		ips = [storage.devicesARP[x][0] for x in range(len(storage.devicesARP))]
		hostNames = [storage.devicesARP[x][1] for x in range(len(storage.devicesARP))]

		if (any(x in ips for x in host[2]) and not(host[0] in hostNames)):

			storage.devicesARP[ips.index(host[2][0])] = [host[2][0], host[0]]

		elif not(any(x in ips for x in host[2])):

			storage.devicesARP.append([host[2][0], host[0]])

	except Exception as e:

		storage.devicesARP.append([host[2][0], "Unable to Find"])

		pass

	return ip

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

	ips = [storage.devicesARP[x][0] for x in range(len(storage.devicesARP))]

	for i in arr:

		if not(i in ips):

			storage.devicesARP.pop(ips.index(i))
			ips = [storage.devicesARP[x][0] for x in range(len(storage.devicesARP))]

def arpsearch ():

	search = 1

	while True:

		if (storage.exit):

			break

		with open("log.txt", 'a') as f:

			f.write(f"Starting Search {search}\n\n")

		toBeSearched = []

		for i in netifaces.ifaddresses('en0')[netifaces.AF_INET]:

			toBeSearched.append(ipaddress.IPv4Network(convertToCIDR(i['addr'], i['netmask']), strict = False))

		with open("log.txt", 'a') as f:

			f.write(f"Ip Ranges: {toBeSearched}\n\n")

		updated = []
		ether = Ether(dst = "ff:ff:ff:ff:ff:ff")

		for i in toBeSearched:

			for j in i:

				packet = ether/ARP(pdst = str(j))

				result = srp(packet, timeout = 3, verbose = 0)[0]

				for sent, received in result:

				    updated.append(findHost(received.psrc))

		clean(scrub(updated))

		with open("log.txt", 'a') as f:

			f.write(f"Updated Hosts: {[storage.devicesARP[x][1] for x in range(len(storage.devicesARP))]}\nHost List has a length of {len(storage.devicesARP)}\n\n")

		search += 1

		time.sleep(1)

	with open("log.txt", 'a') as f:

		f.write(f"Done\n\n")