import queue
import curses
import client
import storage
import controlLoop

client = client()

tClient = threading.Thread(target = client.run, args = [], daemon = True)
tClient.start()

term = curses.initscr()
curses.noecho()
term.refresh()

cmd = [""]

def safeScroll (term):

	try:

		term.move(term.getyx()[0] + 1, 0)

	except:

		term.scrollok(True)
		term.scroll()
		term.scrollok(False)

		term.move(term.getyx()[0], 0)

term.addstr("> ")

while (True):

	c = term.getch()

	if (c == 10):

		safeScroll(term)

		rsp = controlLoop.evaluate(term, cmd[-1])

		if (rsp == "end"):

			break

		elif (rsp == "err"):

			continue

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

							safeScroll(term)

					elif (msg[0] == "E"):

						term.addstr(f"Error: {msg[1]}")

						safeScroll(term)

	else:

		term.addstr(chr(c))

	cmd[-1] = cmd[-1] + chr(c)

curses.endwin()