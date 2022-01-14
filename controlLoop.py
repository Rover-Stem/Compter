import queue
import storage

def scrub (arr):

	arr = list(filter(None, arr))

	return arr

def evaluate (term, cmd):

	cmd = cmd.lower().split(" ")

	if (cmd[0] == "run"):

		if (cmd[1] == "file"):

			cmdSet = []

			with open(cmd[2], 'r') as f:

				cmdSet = f.read().split("\n")

			for i in range(0, len(cmdSet)):

				cmdSet[i] = cmdSet[i].split(" ")

			cmdSet = scrub(cmdSet)

			storage.messagesOut.put("F")

			for i in cmdSet:

				storage.messagesOut.put(i)

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

		if (cmd[2] == "RPI"):

			storage.messagesOut.put(f"L,{cmd[1]}")

			return "sent"

		return "ls"

	elif (cmd[0] == "read"):

		if (cmd[1] == "img"):

			return "img"

	elif (cmd[0] == "h" or cmd[0] == "help"):

		return "help"

	else:

		return "err"
