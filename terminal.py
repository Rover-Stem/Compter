import os
import cv2
import queue
import curses
import storage
import threading

import numpy as np
#from client import client
from controlLoop import evaluate

#client = client()

#tClient = threading.Thread(target = client.run, args = [], daemon = True)
#tClient.start()

os.system('cls' if os.name == 'nt' else 'clear')

term = curses.initscr()
curses.start_color()
curses.noecho()

curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

term.refresh()

cmd = [""]
orig = None
entry = -1
character = -1

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

def printStatusUpdate (statusUpdate):

	term.addstr(str(statusUpdate))

	safeScroll()

	term.addstr("Motors: ")

	if (statusUpdate[2][1]):

		if (curses.has_colors()):

			if not(statusUpdate[2][2]):

				term.addstr("Operational", curses.color_pair(1))

			else:

				term.addstr("Offline", curses.color_pair(2))

		else:

			if not(statusUpdate[2][2]):

				term.addstr("Operational")

			else:

				term.addstr("Offline")

	else:

		if (curses.has_colors()):

			term.addstr("Not Required Currently", curses.color_pair(3))

		else:

			term.addstr("Not Required Currently")

	safeScroll()

	term.addstr("Camera: ")

	if (statusUpdate[3][1]):

		if (curses.has_colors()):

			if not(statusUpdate[3][2]):

				term.addstr("Operational", curses.color_pair(1))

			else:

				term.addstr("Offline", curses.color_pair(2))

		else:

			if not(statusUpdate[3][2]):

				term.addstr("Operational")

			else:

				term.addstr("Offline")

	else:

		if (curses.has_colors()):

			term.addstr("Not Required Currently", curses.color_pair(3))

		else:

			term.addstr("Not Required Currently")

	safeScroll()

	term.addstr("Magnetometer and Accelerometer: ")

	if (statusUpdate[4][1]):

		if (curses.has_colors()):

			if not(statusUpdate[4][2]):

				term.addstr("Operational", curses.color_pair(1))

			else:

				term.addstr("Offline", curses.color_pair(2))

		else:

			if not(statusUpdate[4][2]):

				term.addstr("Operational")

			else:

				term.addstr("Offline")

	else:

		if (curses.has_colors()):

			term.addstr("Not Required Currently", curses.color_pair(3))

		else:

			term.addstr("Not Required Currently")

	safeScroll()

	term.addstr("Servo: ")

	if (statusUpdate[5][1]):

		if (curses.has_colors()):

			if not(statusUpdate[5][2]):

				term.addstr("Operational", curses.color_pair(1))

			else:

				term.addstr("Offline", curses.color_pair(2))

		else:

			if not(statusUpdate[5][2]):

				term.addstr("Operational")

			else:

				term.addstr("Offline")

	else:

		if (curses.has_colors()):

			term.addstr("Not Required Currently", curses.color_pair(3))

		else:

			term.addstr("Not Required Currently")

	safeScroll()

	term.addstr("Ultrasonic Sensor: ")

	if (statusUpdate[6][1]):

		if (curses.has_colors()):

			if not(statusUpdate[6][2]):

				term.addstr("Operational", curses.color_pair(1))

			else:

				term.addstr("Offline", curses.color_pair(2))

		else:

			if not(statusUpdate[6][2]):

				term.addstr("Operational")

			else:

				term.addstr("Offline")

	else:

		if (curses.has_colors()):

			term.addstr("Not Required Currently", curses.color_pair(3))

		else:

			term.addstr("Not Required Currently")

	safeScroll()

#while True:

#	if not(storage.messagesIn.empty()):

#		statusUpdate = storage.messagesIn.get().split(",")

#		for i in range(0, len(statusUpdate)):

#			statusUpdate[i] = statusUpdate[i].split(":")

#			for j in range(0, len(statusUpdate[i])):

#				if (statusUpdate[i][j] == "True"):

#					statusUpdate[i][j] = True

#				elif (statusUpdate[i][j] == "False"):

#					statusUpdate[i][j] = False

#		printStatusUpdate(statusUpdate)

#		break

term.addstr("> ")

while True:

	c = term.getch()

	if (c == 10):

		safeScroll()

		cursor = term.getyx()

		rsp = evaluate(term, cmd[entry])

		if (rsp == "end"):

			break

		elif (rsp == "err"):

			term.addstr(f"Error not valid (Check to see if in testing mode): {cmd[entry]}")
			safeScroll()
			term.addstr("> ")

		elif (rsp == "help"):

			input = cmd[entry]
			command = input.split(" ")

			try:

				if (command[1] == "list"):

					term.addstr("List:")
					safeScroll()
					term.addstr("Usage: ls PATH")
					safeScroll()

					term.addstr("> ")

				elif (command[1] == "read"):

					term.addstr("Read:")
					safeScroll()
					term.addstr("Usage: read img PATH FORMAT")
					safeScroll()

					term.addstr(" ASCII: \"ascii\": Displays image in ASCII format")
					safeScroll()
					term.addstr(" REAL: \"real\": Displays image in seperate window that will close when q is pressed")
					safeScroll()

					term.addstr("> ")

				elif (command[1] == "run"):

					term.addstr("Run:")
					safeScroll()
					term.addstr("Usage: run OPTION [args]")
					safeScroll()

					term.addstr(" Move: \"m\": Moves rover in accordance with the movement option")
					safeScroll()
					term.addstr("  Usage: run m [MOVEMENT OPTION] [TIME] [RATIO] [THROTTLE]")
					safeScroll()
					term.addstr(" Move Distance: \"md\": Moves rover forwards for a certain distance")
					safeScroll()
					term.addstr("  Usage: run md [DISTANCE] [CM]")
					safeScroll()
					term.addstr(" Move Servo: \"ms\": Moves the servo to percent of range of motion")
					safeScroll()
					term.addstr("  Usage: run ms [ANGLE]")
					safeScroll()
					term.addstr(" Get Distance: \"gd\": Gets the distance from the ultra sonic servo")
					safeScroll()
					term.addstr("  Usage: run gd")
					safeScroll()
					term.addstr(" Get Average Distance: \"gad\": Gets the distance from the ultra sonic servo over multiple readings and averages them")
					safeScroll()
					term.addstr("  Usage: run gad [TIME BETWEEN PULSES] [NUMBER OF PULSES]")
					safeScroll()
					term.addstr(" Get Magnetometer: \"gm\": Gets the magnetometer reading")
					safeScroll()
					term.addstr("  Usage: run gm")
					safeScroll()
					term.addstr(" Get Acceleration: \"ga\": Gets the accelerometer reading")
					safeScroll()
					term.addstr("  Usage: run ga")
					safeScroll()
					term.addstr(" Take Picture: \"tp\": Takes picture and sends it to the host computer")
					safeScroll()
					term.addstr("  Usage: run tp")
					safeScroll()

					term.addstr("> ")

				else:

					term.addstr(f"{command[1].capitalize()} is not a valid help option")
					safeScroll()
					term.addstr("> ")

			except:

				term.addstr("(Note for more specific notes on commands enter help and then the command Ex. help run or help run m)")
				safeScroll()
				term.addstr(f"Options: ")
				safeScroll()

				term.addstr(" Exit: \"exit\": Quits the terminal and cuts the connection")
				safeScroll()
				term.addstr(" List: \"ls\": Lists files in directory either local or on the rover")
				safeScroll()
				term.addstr(" Read: \"read\": Used for reading images and displaying them in ASCII or as the standard image")
				safeScroll()
				term.addstr(" Run: \"run\": Runs command on the rover valid for all options but list")
				safeScroll()

				term.addstr("> ")

		elif (rsp == "ls"):

			try:

				input = cmd[entry]
				command = input.split(" ")

				programsList = []

				for i in os.listdir(f"./{command[1]}"):

					programsList.append(i + "")

				programsList.sort()

				for i in programsList:

					term.addstr(f"{i}")
					safeScroll()

				term.addstr("> ")

			except:

				term.addstr("File Path Error")
				safeScroll()
				term.addstr("> ")

		elif (rsp == "img"):

			try:

				input = cmd[entry]
				command = input.lower().split(" ")

				img_orig = cv2.imread(f"./{command[2]}")

				if (command[3] == "ascii"):

					min_size_x = 130
					min_size_y = 130

					x_or_y = True

					gradient = ["█", "$", "@", "B", "%", "8", "&", "W", "M", "#", "*", "o", "a", "h", "k", "b", "d", "p", "q", "w", "m", "Z", "O", "0", "Q", "L", "C", "J", "U", "Y", "X", "z", "c", "v", "u", "n", "x", "r", "j", "f", "t", "/", "\\", "|", "(", ")", "1", "{", "}", "[", "]", "?", "-", "_", "+", "~", "<", ">", "i", "!", "l", "I", ";", ":", ",", "\"", "^", "`", "'", ".", " "]

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

							term.addstr(f"{final_ascii[i][j]}")

						safeScroll()

					term.addstr("> ")

				elif (command[3] == "real"):

					cv2.imshow('image',img_orig)
					cv2.waitKey("q")
					cv2.destroyAllWindows()
					term.addstr("> ")

			except:

				term.addstr("File Path Error")
				safeScroll()
				term.addstr("> ")

		else:

			while True:

				if not(storage.messagesIn.empty()):

					msg = storage.messagesIn.get().split(",")

					if (msg[0] == "F"):

						term.addstr("> ")

						break

					elif (msg[0] == "S"):

						if (msg[1] == "D"):

							term.addstr(f"Distance: {msg[2]}")

							safeScroll()

						elif (msg[1] == "AD"):

							term.addstr(f"Average Distance was {msg[2]} over {msg[3]} pings which were {msg[4]} sec apart")

							safeScroll()

						elif (msg[1] == "M"):

							term.addstr(f"Magnetic Reading: {str(msg[2])}")

							safeScroll()

						elif (msg[1] == "A"):

							term.addstr(f"Acceleration: {msg[2]}")

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

							term.addstr(f"{msg[2]}")
							safeScroll()

						else:

							term.addstr(f"Status: {msg[1]}")
							safeScroll()

					elif (msg[0] == "E"):

						term.addstr(f"Error: {msg[1]}")

						safeScroll()

		if not(entry == -1):

			temp = cmd[entry]
			cmd[entry] = orig
			cmd[-1] = temp

		cmd.append("")
		entry = -1

	elif (c == 8 or c == 127):

		try:

			temp_cursor = term.getyx()

			term.move(temp_cursor[0], 0)

			term.clrtoeol()

			if not(character == -1):

				if ((character * -1) > len(cmd[entry])):

					term.addstr("> " + cmd[entry])
					term.move(temp_cursor[0], temp_cursor[1])

				else:

					cmd[entry] = cmd[entry][:character] + cmd[entry][character + 1:]
					term.addstr("> " + cmd[entry])
					term.move(temp_cursor[0], temp_cursor[1] - 1)

			else:

				cmd[entry] = cmd[entry][:character]
				term.addstr("> " + cmd[entry])

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

				term.addstr("> " + cmd[entry])

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

				term.addstr("> " + cmd[entry])

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

		elif ((character * -1) > len(cmd[entry])):

			cmd[entry] = chr(c) + cmd[entry]

			temp_cursor = term.getyx()

			term.move(temp_cursor[0], 0)

			term.clrtoeol()

			term.addstr("> " + cmd[entry])

			term.move(temp_cursor[0], temp_cursor[1] + 1)

			character += 1

			continue

		else:

			cmd[entry] = cmd[entry][:character + 1] + chr(c) + cmd[entry][character + 1:]

		temp_cursor = term.getyx()

		term.move(temp_cursor[0], 0)

		term.clrtoeol()

		term.addstr("> " + cmd[entry])

curses.endwin()

os.system('cls' if os.name == 'nt' else 'clear')