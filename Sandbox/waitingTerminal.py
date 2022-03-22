import time
import curses
import storage
import ipSearch
import arpSearch
import threading
import subprocess

from datetime import datetime

def safeScroll (term):

	try:

		temp_cursor = term.getyx()
		term.move(temp_cursor[0] + 1, 0)

	except:

		term.scrollok(True)
		term.scroll()
		term.scrollok(False)

		temp_cursor = term.getyx()
		term.move(temp_cursor[0], 0)

def safePrint (text, term, color = None):

	rows, cols = term.getmaxyx()

	if (len(text) > (cols - 2)):

		if (color == None):

			term.addstr(text[:(cols - 2)])
			safeScroll(term)

		else:

			term.addstr(text[:(cols - 2)], color)
			safeScroll(term)

		i = 0

		while True:

			if ((len(text) - (cols * i) - (cols - 2)) > cols):

				if (color == None):

					term.addstr(text[((cols - 2) + (cols * i)):((cols - 2) + (cols * (i + 1)))])

				else:

					term.addstr(text[((cols - 2) + (cols * i)):((cols - 2) + (cols * (i + 1)))], color)

				i += 1

			else:

				break

		if (color == None):

			term.addstr(text[((cols - 2) + (cols * i)):])

		else:

			term.addstr(text[((cols - 2) + (cols * i)):], color)

	else:

		if (color == None):

			term.addstr(text)

		else:

			term.addstr(text, color)

def run ():

	with open("log.txt", 'a') as f:

		f.write(f"Term init\n\n")

	term = curses.initscr()
	term.nodelay(1)
	curses.noecho()
	curses.start_color()

	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

	term.refresh()

	with open("log.txt", 'a') as f:

		f.write(f"Starting Term\n\n")

	f = open("Animations/waitingTerm.animation", 'r')

	animation = f.read().split("\n")

	animationPointers = []

	for i in range(len(animation)):

		try:

			animationPointers.append([float(animation[i]), i])

		except:

			pass

	character = ""

	animationStartTime = datetime.now()
	animationCurrentTime = datetime.now()
	searchingStartTime = datetime.now()
	searchingCurrentTime = datetime.now()

	tDevice = threading.Thread(target = ipSearch.ipsearch, args = [], daemon = True)
	tDevice.start()
	tDevice = threading.Thread(target = arpSearch.arpsearch, args = [], daemon = True)
	tDevice.start()

	while True:

		if (storage.connected == True):

			break

		else:

			process = subprocess.Popen(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport','-I'], stdout = subprocess.PIPE)
			out, err = process.communicate()
			process.wait()

			out = out.decode("UTF-8").split("\n")

			term.clear()

			animationDifference = (animationCurrentTime - animationStartTime).seconds
			searchingDifference = (searchingCurrentTime - searchingStartTime).seconds

			if (animationDifference > animationPointers[-2][0]):

				animationStartTime = datetime.now()

				animationDifference = (animationCurrentTime - animationStartTime).seconds

			for i in range((len(animationPointers) - 1)):

				if ((animationDifference >= animationPointers[i][0]) and (animationDifference < animationPointers[i + 1][0])):

					for j in range((animationPointers[i][1] + 1), animationPointers[i + 1][1]):

						safePrint(animation[j], term)
						safeScroll(term)

					break

			if ((searchingDifference >= 0) and (searchingDifference < 1)):

				safePrint("Searching", term)

			elif ((searchingDifference >= 1) and (searchingDifference < 2)):

				safePrint("Searching.", term)

			elif ((searchingDifference >= 2) and (searchingDifference < 3)):

				safePrint("Searching..", term)

			elif ((searchingDifference >= 3) and (searchingDifference < 4)):

				safePrint("Searching...", term)

			else:

				safePrint("Searching...", term)
				searchingStartTime = datetime.now()

			safeScroll(term)
			safeScroll(term)

			for i in range(len(out)):

				out[i] = out[i].split(": ")

			for i in out:

				if (("SSID" in i[0]) and not("BSSID" in i[0])):

					safePrint(f"WIFI: {i[1]}", term, 1)

					break

			safeScroll(term)
			safeScroll(term)

			safePrint("Devices on network:", term)
			safeScroll(term)

			for i in storage.devicesARP:

				safePrint(f"{i[1]} - {i[0]}", term)
				safeScroll(term)

			for i in storage.devicesIP:

				safePrint(f"{i[1]} - {i[0]}", term)
				safeScroll(term)

			safeScroll(term)
			safePrint(f"Exit (Y/N)? {character}", term)

			temp = term.getch()

			if (temp != -1):

				if (str(chr(temp)).lower() in ["y", "n", "\n"]):

					character += chr(temp)

			if ("\n" in character):

				if (character.lower()[0] == "y"):

					storage.exit = True
					break

				else:

					character = ""

			term.refresh()

			animationCurrentTime = datetime.now()
			searchingCurrentTime = datetime.now()

	with open("log.txt", 'a') as f:

		f.write(f"Ending Term\n\n")

	curses.endwin()