import os
import queue
import curses
import storage
import threading

#from client import client
#from controlLoop import evaluate

#client = client()

#tClient = threading.Thread(target = client.run, args = [], daemon = True)
#tClient.start()

term = curses.initscr()
curses.noecho()
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

term.addstr("> ")

while (True):

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

							term.addstr(f"Average Distance was {msg[2]} over {msg[3]} pings which were {msg[4]}sec apart")

							safeScroll()

						elif (msg[1] == "M"):

							term.addstr(f"Magnetic Reading: {msg[2]}")

							safeScroll()

						elif (msg[1] == "A"):

							term.addstr(f"Acceleration: {msg[2]}")

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