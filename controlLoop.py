import queue
import storage

def scrub (arr):

	arr = list(filter(None, arr))

	return arr

def evaluate (term, cmd):

	cmd = scrub(cmd.lower().split(" "))

	try:

		if (cmd[0] == "run"):

			if (cmd[1] == "file"):

				if (cmd[2] == "l"):

					storage.messagesOut.put("F,l")

				elif (cmd[2] == "s"):

					cmdSet = []

					with open(cmd[2], 'r') as f:

						cmdSet = f.read().split("\n")

					for i in range(0, len(cmdSet)):

						cmdSet[i] = cmdSet[i].split(" ")

					cmdSet = scrub(cmdSet)

					storage.messagesOut.put("F,s")

					for i in cmdSet:

						storage.messagesOut.put(i)

				else:

					storage.messagesOut.put(f"F,{cmd[2]}")

			else:

				args = ""

				for i in cmd:

					if (i == "run"):

						continue

					args += "," + i

				storage.messagesOut.put(f"R{args}")

			return "sent"

		elif (cmd[0] == "exit"):

			storage.messagesOut.put("stop")

			while True:

				if not(storage.messagesOut.empty()):

					break

			return "end"

		elif (cmd[0] == "ls"):

			try:

				if (cmd[2] == "rpi"):

					storage.messagesOut.put(f"L,{cmd[1]}")

					return "sent"

				elif (cmd[2] == "loc"):

					return "ls"

				else:

					return "err"

			except:

				try:

					storage.messagesOut.put(f"L,{cmd[1]}")

					return "sent"

				except:

					return "err"

		elif (cmd[0] == "read"):

			if (cmd[1] == "img"):

				return "img"

		elif (cmd[0] == "h" or cmd[0] == "help"):

			return "help"

		elif (cmd[0] == "clear"):

			return "clr"

		else:

			return "err"

	except:

		return "err"
