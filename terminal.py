import os
import cv2
import sys
import queue
import curses
import storage
import threading

import numpy as np
from client import client
from controlLoop import evaluate

# Sorts list by file type
def sortByFileType (arr):

	temp = [[[], "a"]]
	temp2 = []

	for i in arr:

		if (i.split(".")[-1] in [x[1] for x in temp]):

			for j in temp:

				if ((i.split(".")[-1] == j[1]) and not(i.split(".")[0] == j[1])):

					j[0].append(i)

		else:

			if (i.split(".")[0] == i.split(".")[-1]):

				for j in temp:

					if (j[1] == "a"):

						j[0].append(i)

			else:

				temp.append([[i], i.split(".")[-1]])

	for j in temp:

		j[0].sort()

	fileTypes = [x[1] for x in temp]

	fileTypes.sort()

	for i in fileTypes:

		for j in temp:

			if j[1] == i:

				for l in j[0]:

					temp2.append(l)

				break

		continue

	return temp2

def safeScroll ():

	try:

		temp_cursor = term.getyx()
		term.move(temp_cursor[0] + 1, 0)

	except:

		term.scrollok(True)
		term.scroll()
		term.scrollok(False)

		temp_cursor = term.getyx()
		term.move(temp_cursor[0], 0)

def safePrint (text, color = None):

	rows, cols = term.getmaxyx()

	if (len(text) > (cols - 2)):

		if (color == None):

			term.addstr(text[:(cols - 2)])
			safeScroll()

		else:

			term.addstr(text[:(cols - 2)], color)
			safeScroll()

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

def printStatusUpdate (statusUpdate):

	safePrint(str(statusUpdate))

	safeScroll()

	safePrint("Motors: ")

	if (statusUpdate[2][1]):

		if (curses.has_colors()):

			if not(statusUpdate[2][2]):

				safePrint("Operational", curses.color_pair(1))

			else:

				safePrint("Offline", curses.color_pair(2))

		else:

			if not(statusUpdate[2][2]):

				safePrint("Operational")

			else:

				safePrint("Offline")

	else:

		if (curses.has_colors()):

			safePrint("Not Required Currently", curses.color_pair(3))

		else:

			safePrint("Not Required Currently")

	safeScroll()

	safePrint("Camera: ")

	if (statusUpdate[3][1]):

		if (curses.has_colors()):

			if not(statusUpdate[3][2]):

				safePrint("Operational", curses.color_pair(1))

			else:

				safePrint("Offline", curses.color_pair(2))

		else:

			if not(statusUpdate[3][2]):

				safePrint("Operational")

			else:

				safePrint("Offline")

	else:

		if (curses.has_colors()):

			safePrint("Not Required Currently", curses.color_pair(3))

		else:

			safePrint("Not Required Currently")

	safeScroll()

	safePrint("Magnetometer and Accelerometer: ")

	if (statusUpdate[4][1]):

		if (curses.has_colors()):

			if not(statusUpdate[4][2]):

				safePrint("Operational", curses.color_pair(1))

			else:

				safePrint("Offline", curses.color_pair(2))

		else:

			if not(statusUpdate[4][2]):

				safePrint("Operational")

			else:

				safePrint("Offline")

	else:

		if (curses.has_colors()):

			safePrint("Not Required Currently", curses.color_pair(3))

		else:

			safePrint("Not Required Currently")

	safeScroll()

	safePrint("Servo: ")

	if (statusUpdate[5][1]):

		if (curses.has_colors()):

			if not(statusUpdate[5][2]):

				safePrint("Operational", curses.color_pair(1))

			else:

				safePrint("Offline", curses.color_pair(2))

		else:

			if not(statusUpdate[5][2]):

				safePrint("Operational")

			else:

				safePrint("Offline")

	else:

		if (curses.has_colors()):

			safePrint("Not Required Currently", curses.color_pair(3))

		else:

			safePrint("Not Required Currently")

	safeScroll()

	safePrint("Time of Flight Sensor: ")

	if (statusUpdate[6][1]):

		if (curses.has_colors()):

			if not(statusUpdate[6][2]):

				safePrint("Operational", curses.color_pair(1))

			else:

				safePrint("Offline", curses.color_pair(2))

		else:

			if not(statusUpdate[6][2]):

				safePrint("Operational")

			else:

				safePrint("Offline")

	else:

		if (curses.has_colors()):

			safePrint("Not Required Currently", curses.color_pair(3))

		else:

			safePrint("Not Required Currently")

	safeScroll()

# Loads Commands from cmds.local file
def loadCommands ():

	with open("cmds.local", 'r') as cmdFile:

		lines = cmdFile.read()

		linesSplit = lines.split(",")

		with open("log.txt", 'a') as f:

			f.write(f"Previous Commands: {linesSplit}\n\n")

		cmdNums = len(linesSplit)

		return linesSplit

	return []

# Stores Commands to cmds.local file
def storeCommands (cmds):

	with open("cmds.local", 'a') as cmdFile:

		cmdFile.truncate(0)

		for i in range(len(cmds)):

			if (i < (cmdNums - 1)):

				continue

			if not(cmds[i] == ""):

				cmdFile.write(f",{cmds[i]}")

with open("log.txt", 'a') as f:

	f.truncate(0)
	f.close()

args = sys.argv[1:]
testing = False
logging = False
hostIn = "raspberrypi.local"
portIn = 1234
packetSizeIn = 1024

for i in args:

	if (("-" in i) and (("t" in i) or ("l" in i))):

		if ("t" in i):

			testing = True

		if ("l" in i):

			logging = True

	if ("host" in i.lower()):

		hostIn = i.lower().replace(" ", "").split("=")[1]

	if ("port" in i.lower()):

		portIn = i.lower().replace(" ", "").split("=")[1]

	if ("packet" in i.lower()):

		packetSizeIn = i.lower().replace(" ", "").split("=")[1]

with open("log.txt", 'a') as f:

	f.write(f"Found args and starting client\n")

client = client(testing, hostIn, portIn, packetSizeIn)

if (storage.exit):

	with open("log.txt", 'a') as f:

		f.write(f"Exited in searching window\n")

	os.system('cls' if os.name == 'nt' else 'clear')

	sys.exit()

with open("log.txt", 'a') as f:

	f.write(f"Client Initiallized\n")

tClient = threading.Thread(target = client.run, args = [], daemon = True)
tClient.start()

with open("log.txt", 'a') as f:

	f.write(f"Client Running\n")

os.system('cls' if os.name == 'nt' else 'clear')

term = curses.initscr()
curses.start_color()
curses.noecho()

curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

term.refresh()

cmd = loadCommands() + [""]
cmdNums = 0
orig = None
inputActive = False
entry = -1
character = -1

if (logging and not(testing)):

	storage.messagesOut.put(f"S")

elif (logging and testing):

	safePrint("Logging Was Not Enabled: Cannot Log In Testing Mode", curses.color_pair(2))
	safeScroll()

if (testing):

	safePrint("In Testing Mode", curses.color_pair(1))
	safeScroll()

else:

	while True:

		if not(storage.messagesIn.empty()):

			statusUpdate = storage.messagesIn.get().split(",")

			for i in range(0, len(statusUpdate)):

				statusUpdate[i] = statusUpdate[i].split(":")

				for j in range(0, len(statusUpdate[i])):

					if (statusUpdate[i][j] == "True"):

						statusUpdate[i][j] = True

					elif (statusUpdate[i][j] == "False"):

						statusUpdate[i][j] = False

			printStatusUpdate(statusUpdate)

			break

safePrint("> ")

while True:

	c = term.getch()

	if (c == 10):

		with open("log.txt", 'a') as f:

			f.write(f"Working with: {cmd[entry]}\n")

		cursor = term.getyx()

		rsp = evaluate(term, cmd[entry])

		safeScroll()

		with open("log.txt", 'a') as f:

			f.write(f"Responded with: {rsp}\n\n")

		if (inputActive):

			inputActive = False
			storage.messagesOut.put(cmd[entry])
			safePrint("> ")

		elif (rsp == "end"):

			break

		elif (rsp == "err"):

			safePrint(f"Not valid: \"{cmd[entry]}\"")
			safeScroll()
			safePrint("> ")

		elif (rsp == "clr"):

			term.clear()
			safePrint("> ")

		elif (rsp == "log" and not(logging)):

			storage.messagesOut.put("S")
			logging = True
			safePrint("> ")

		elif (rsp == "help"):

			input = cmd[entry]
			command = input.split(" ")

			try:

				if (command[1] == "ls"):

					safePrint("List:")
					safeScroll()
					safePrint("Usage: ls PATH [RPI or loc]")
					safeScroll()

					safePrint("> ")

				elif (command[1] == "read"):

					safePrint("Read:")
					safeScroll()
					safePrint("Usage: read img PATH FORMAT")
					safeScroll()

					safePrint("Formats:")
					safeScroll()
					safePrint(" ASCII: \"ascii\": Displays image in ASCII format")
					safeScroll()
					safePrint(" REAL: \"real\": Displays image in seperate window that will close when q is pressed")
					safeScroll()

					safePrint("> ")

				elif (command[1] == "run"):

					safePrint("Run:")
					safeScroll()
					safePrint("Usage: run OPTION [args]")
					safeScroll()

					safePrint(" Move: \"m\": Moves rover in accordance with the movement option")
					safeScroll()
					safePrint("  Usage: run m [MOVEMENT OPTION] [TIME] [RATIO] [THROTTLE]")
					safeScroll()
					safePrint(" Move Distance: \"md\": Moves rover forwards for a certain distance")
					safeScroll()
					safePrint("  Usage: run md [DISTANCE] [CM]")
					safeScroll()
					safePrint(" Move To Angle: \"ma\": Moves rover to a certain angle")
					safeScroll()
					safePrint("  Usage: run ma [ANGLE] [RADS]")
					safeScroll()
					safePrint(" Move Servo: \"ms\": Moves the servo to percent of range of motion")
					safeScroll()
					safePrint("  Usage: run ms [ANGLE]")
					safeScroll()
					safePrint(" Get Distance: \"gd\": Gets the distance from the time of flight sensor")
					safeScroll()
					safePrint("  Usage: run gd")
					safeScroll()
					safePrint(" Get Average Distance: \"gad\": Gets the distance from the time of flight sensor over multiple readings and averages them")
					safeScroll()
					safePrint("  Usage: run gad [NUMBER OF MEASUREMENTS]")
					safeScroll()
					safePrint(" Get Magnetometer: \"gm\": Gets the magnetometer reading")
					safeScroll()
					safePrint("  Usage: run gm")
					safeScroll()
					safePrint(" Get Acceleration: \"ga\": Gets the accelerometer reading")
					safeScroll()
					safePrint("  Usage: run ga")
					safeScroll()
					safePrint(" Get Direction: \"gdir\": Gets the direction from the magnetometer reading")
					safeScroll()
					safePrint("  Usage: run gdir [RADS]")
					safeScroll()
					safePrint(" Take Picture: \"tp\": Takes picture and sends it to the host computer")
					safeScroll()
					safePrint("  Usage: run tp")
					safeScroll()
					safePrint(" Run Preset: \"preset\": Runs preset")
					safeScroll()
					safePrint("  Usage: run preset [OPTION]")
					safeScroll()
					safePrint(" Run Live: \"live\": Runs live control")
					safeScroll()
					safePrint("  Usage: run live")
					safeScroll()

					safePrint("> ")

				elif (command[1] == "preset"):

					safePrint("Preset:")
					safeScroll()
					safePrint("Usage: run preset OPTION [args]")
					safeScroll()

					safePrint(" Square: \"square\": Moves the rover in a square")
					safeScroll()
					safePrint("  Usage: run preset square")
					safeScroll()
					safePrint(" Distance Challange: \"distanceChallenge\": Moves the rover to the given distance")
					safeScroll()
					safePrint("  Usage: run preset distanceChallenge [DISTANCE]")
					safeScroll()
					safePrint(" Direction Challange: \"directionChallenge\": Moves the rover to a certain angle before moving forwards")
					safeScroll()
					safePrint("  Usage: run preset directionChallenge [ANGLE] [RADS]")
					safeScroll()
					safePrint(" Obstacle Avoidance 1 (Stopping): \"obstacleAvoidance1\": Moves the rover and then stops the rover when an object is detected")
					safeScroll()
					safePrint("  Usage: run preset obstacleAvoidance1")
					safeScroll()
					safePrint(" Obstacle Avoidance 2 (Moving Around): \"obstacleAvoidance2\": Moves the rover and goes around an obstacle when detected")
					safeScroll()
					safePrint("  Usage: run preset obstacleAvoidance2 [NUMBER OF OBSTACLES]")
					safeScroll()
					safePrint(" Parallel Parking: \"parallelParking\": Parallel parks the rover")
					safeScroll()
					safePrint("  Usage: run preset parallelParking [LEFT]")
					safeScroll()
					safePrint(" Stay In Your Lane: \"stayInYourLane\": Moves the rover and keeps it within detected lines")
					safeScroll()
					safePrint("  Usage: run preset stayInYourLane")
					safeScroll()
					safePrint(" Navigate The Neighborhood: \"navNeighborhood\": Moves the rover through a neighborhood with binary coded intersections")
					safeScroll()
					safePrint("  Usage: run preset navNeighborhood")
					safeScroll()

					safePrint("> ")

				elif (command[1] == "FORMAT"):

					safePrint("Formats:")
					safeScroll()
					safePrint(" ASCII: \"ascii\": Displays image in ASCII format")
					safeScroll()
					safePrint(" REAL: \"real\": Displays image in seperate window that will close when q is pressed")
					safeScroll()

					safePrint("> ")

				elif (command[1] == "ANGLE"):

					safePrint("Desired angle as a percent of the movement for servo - Must be a number between -1 and 1 (Non-Inclusive)")
					safeScroll()
					safePrint("OR")
					safeScroll()
					safePrint("Desired angle in radians or degrees")
					safeScroll()

					safePrint("> ")

				elif (command[1] == "PATH"):

					safePrint("Path to desired file - Note: ./ is automatically added as a prefix")
					safeScroll()

					safePrint("> ")

				elif (command[1] == "DISTANCE"):

					safePrint("Distance in desired units (in or cm)")
					safeScroll()

					safePrint("> ")

				elif (command[1] == "CM"):

					safePrint("Set to True if distance is in centimeters")
					safeScroll()

					safePrint("> ")

				elif (command[1] == "RADS"):

					safePrint("Set to True if direction in radians is desired")
					safeScroll()

					safePrint("> ")

				elif (command[1] == "LEFT"):

					safePrint("Set to True if parallel parking is on the left")
					safeScroll()

					safePrint("> ")

				elif (command[1] == "MOVEMENT"):

					safePrint("Movement Options:")
					safeScroll()
					safePrint(" f - Forwards")
					safeScroll()
					safePrint(" b - Backwards")
					safeScroll()
					safePrint(" r - Right")
					safeScroll()
					safePrint(" l - Left")
					safeScroll()
					safePrint(" dfr - Diagnonal Forwards Right")
					safeScroll()
					safePrint(" dfl - Diagnonal Forwards Left")
					safeScroll()
					safePrint(" dbr - Diagnonal Backwards Right")
					safeScroll()
					safePrint(" dbl - Diagnonal Backwards Left")
					safeScroll()
					safePrint(" cfr - Curve Forwards Right")
					safeScroll()
					safePrint(" cfl - Curve Forwards Left")
					safeScroll()
					safePrint(" cbr - Curve Backwards Right")
					safeScroll()
					safePrint(" cbl - Curve Backwards Left")
					safeScroll()
					safePrint(" rr - Rotate Right")
					safeScroll()
					safePrint(" rl - Rotate Left")
					safeScroll()

					safePrint("> ")

				elif (command[1] == "TIME"):

					safePrint("Time in seconds")
					safeScroll()

					safePrint("> ")

				elif (command[1] == "RATIO"):

					safePrint("Ratio in decimal form from 1 to 0 inclusive")
					safeScroll()

					safePrint("> ")

				elif (command[1] == "THROTTLE"):

					safePrint("Percent of motor speed from 1 to 0 inclusive")
					safeScroll()

					safePrint("> ")

				else:

					safePrint(f"{command[1].capitalize()} is not a valid help option")
					safeScroll()
					safePrint("> ")

			except:

				safePrint("(Note for more specific notes on commands enter help and then the command or argument name Ex. help run or help PATH)")
				safeScroll()
				safePrint(f"Options: ")
				safeScroll()

				safePrint(" Exit: \"exit\": Quits the terminal and cuts the connection")
				safeScroll()
				safePrint(" List: \"ls\": Lists files in directory either locally or on the rover")
				safeScroll()
				safePrint(" Read: \"read\": Used for reading images and displaying them in ASCII or as the standard image")
				safeScroll()
				safePrint(" Run: \"run\": Runs command on the rover valid for all options but list")
				safeScroll()
				safePrint(" Start Logging: \"start logs\": Starts logging on the rover")
				safeScroll()
				safePrint(" Clear: \"clear\": Clears terminal")
				safeScroll()

				safePrint("> ")

		elif (rsp == "ls"):

			safeScroll()

			try:

				input = cmd[entry]
				command = input.split(" ")

				programsList = []

				for i in os.listdir(f"./{command[1]}"):

					programsList.append(i + "")

				programsList = sortByFileType(programsList)

				for i in programsList:

					safePrint(f"{i}")
					safeScroll()

				safePrint("> ")

			except:

				safePrint("File Path Error")
				safeScroll()
				safePrint("> ")

		elif (rsp == "img"):

			try:

				input = cmd[entry]
				command = input.lower().split(" ")

				img_orig = cv2.imread(f"./{command[2]}")

				if (command[3] == "ascii"):

					min_size_x = 130
					min_size_y = 130

					x_or_y = True

					gradient = ["???", "$", "@", "B", "%", "8", "&", "W", "M", "#", "*", "o", "a", "h", "k", "b", "d", "p", "q", "w", "m", "Z", "O", "0", "Q", "L", "C", "J", "U", "Y", "X", "z", "c", "v", "u", "n", "x", "r", "j", "f", "t", "/", "\\", "|", "(", ")", "1", "{", "}", "[", "]", "?", "-", "_", "+", "~", "<", ">", "i", "!", "l", "I", ";", ":", ",", "\"", "^", "`", "'", ".", " "]

					img = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY)

					if (img.shape[1] > img.shape[0]):

						min_size = int(min_size_x / 2)
						x_or_y = True

					else:

						min_size = int(min_size_x / 2)
						x_or_y = False

					if (x_or_y):

						percent = min_size / img.shape[1]
						new_size = (min_size, int(img.shape[0] * percent))

					else:

						percent = min_size / img.shape[0]
						new_size = (int(img.shape[1] * percent), min_size)

					img_orig = cv2.resize(img_orig, new_size)
					img = cv2.resize(img, new_size)

					img = img * (70 / 255)

					final_ascii = [[]]

					for i in range(0, img.shape[0]):

						for j in range(0, img.shape[1]):

							final_ascii[-1].append(gradient[70 - int(img[i][j])] + " ")

						final_ascii.append([])

					for i in range(0, len(final_ascii)):

						for j in range(0, len(final_ascii[i])):

							safePrint(f"{final_ascii[i][j]}")

						safeScroll()

					safePrint("> ")

				elif (command[3] == "real"):

					cv2.imshow('image',img_orig)
					cv2.waitKey("q")
					cv2.destroyAllWindows()
					safePrint("> ")

			except:

				safePrint("File Path Error")
				safeScroll()
				safePrint("> ")

		else:

			while True:

				#safePrint(f"Messages In: {storage.messagesIn}")

				#safeScroll()

				if not(storage.messagesIn.empty()):

					msg = storage.messagesIn.get().split(",")

					if (msg[0] == "F"):

						safePrint("> ")

						break

					elif (msg[0] == "I"):

						safePrint(" > ")
						inputActive = True

						break

					elif (msg[0] == "S"):

						if (msg[1] == "D"):

							safePrint(f"Distance: {msg[2]}")

							safeScroll()

						elif (msg[1] == "DIR"):

							safePrint(f"Direction: {msg[2]}??")

							safeScroll()

						elif (msg[1] == "AD"):

							safePrint(f"Average Distance was {msg[2]} over {msg[3]} pings which were {msg[4]} sec apart")

							safeScroll()

						elif (msg[1] == "M"):

							safePrint(f"Magnetic Reading:")
							safeScroll()

							safePrint(f" X: {str(msg[2])}")
							safeScroll()

							safePrint(f" Y: {str(msg[3])}")
							safeScroll()

							safePrint(f" Z: {str(msg[4])}")
							safeScroll()

						elif (msg[1] == "A"):

							safePrint(f"Acceleration:")
							safeScroll()

							safePrint(f" X: {str(msg[2])}")
							safeScroll()

							safePrint(f" Y: {str(msg[3])}")
							safeScroll()

							safePrint(f" Z: {str(msg[4])}")
							safeScroll()

						elif (msg[1] == "SU"):

							for i in range(0, len(msg)):

								msg[i] = msg[i].split(":")

								for j in range(0, len(msg[i])):

									if (msg[i][j] == "True"):

										msg[i][j] = True

									elif (msg[i][j] == "False"):

										msg[i][j] = False

							printStatusUpdate(msg)

						elif (msg[1] == "L"):

							if ((msg[2].split(".")[-1] == "py") or (msg[2].split(".")[-1] == "pyc")):

								safePrint(f"{msg[2]}", curses.color_pair(1))
								safeScroll()

							elif (msg[2].split(".")[-1] == msg[2]):

								safePrint(f"{msg[2]}", curses.color_pair(3))
								safeScroll()

							elif (msg[2].split(".")[-1] == "squish"):

								safePrint(f"{msg[2]}", curses.color_pair(2))
								safeScroll()

							else:

								safePrint(f"{msg[2]}")
								safeScroll()

						else:

							safePrint(f"Status: {msg[1]}")
							safeScroll()

					elif (msg[0] == "E"):

						safePrint(f"Error: {msg[1]}")

						safeScroll()

		if not(entry == -1):

			temp = cmd[entry]
			cmd[entry] = orig
			cmd[-1] = temp

		cmd.append("")
		entry = -1
		character = -1

	elif (c == 8 or c == 127):

		try:

			temp_cursor = term.getyx()

			term.move(temp_cursor[0], 0)

			term.clrtoeol()

			if not(character == -1):

				if ((character * -1) > len(cmd[entry])):

					safePrint("> " + cmd[entry])
					term.move(temp_cursor[0], temp_cursor[1])

				else:

					cmd[entry] = cmd[entry][:character] + cmd[entry][character + 1:]
					safePrint("> " + cmd[entry])
					term.move(temp_cursor[0], temp_cursor[1] - 1)

			else:

				cmd[entry] = cmd[entry][:character]
				safePrint("> " + cmd[entry])

		except:

			continue

	elif (c == 27):

		term.nodelay(True)

		c1 = term.getch()
		c2 = term.getch()

		term.nodelay(False)

		full_code = chr(c) + chr(c1) + chr(c2)

		# Up
		if (full_code == "\x1b[A"):

			if not((-1 * (entry - 1)) > len(cmd)):

				entry -= 1

				temp_cursor = term.getyx()
				term.move(temp_cursor[0], 0)

				term.clrtoeol()

				safePrint("> " + cmd[entry])

				character = -1

				if not(entry == -1):

					orig = cmd[entry]

				else:

					orig = None

		# Down
		elif (full_code == "\x1b[B"):

			if not((entry + 1) == 0):

				entry += 1

				temp_cursor = term.getyx()
				term.move(temp_cursor[0], 0)

				term.clrtoeol()

				safePrint("> " + cmd[entry])

				character = -1

				if not(entry == -1):

					orig = cmd[entry]

				else:

					orig = None

		# Right
		elif (full_code == "\x1b[C"):

			temp_cursor = term.getyx()

			try:

				if not((character + 1) == 0):

					character += 1

					term.move(temp_cursor[0], temp_cursor[1] + 1)

			except:

				continue

		# Left
		elif (full_code == "\x1b[D"):

			temp_cursor = term.getyx()

			try:

				if not(-1 * (character - 1) > (len(cmd[entry]) + 1)):

					character -= 1

					term.move(temp_cursor[0], temp_cursor[1] - 1)

			except:

				continue

	else:

		if (character == -1):

			cmd[entry] = cmd[entry] + chr(c)

			temp_cursor = term.getyx()

			term.move(temp_cursor[0], 0)

			term.clrtoeol()

			safePrint("> " + cmd[entry])

		elif ((character * -1) > len(cmd[entry])):

			cmd[entry] = chr(c) + cmd[entry]

			temp_cursor = term.getyx()

			term.move(temp_cursor[0], 0)

			term.clrtoeol()

			safePrint("> " + cmd[entry])

			term.move(temp_cursor[0], temp_cursor[1] + 1)

			character += 1

			continue

		else:

			temp_cursor = term.getyx()

			cmd[entry] = cmd[entry][:character + 1] + chr(c) + cmd[entry][character + 1:]

			term.move(temp_cursor[0], 0)

			term.clrtoeol()

			safePrint("> " + cmd[entry])

			term.move(temp_cursor[0], temp_cursor[1] + 1)

			continue

storeCommands(cmd)

curses.endwin()

os.system('cls' if os.name == 'nt' else 'clear')