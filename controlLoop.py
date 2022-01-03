import queue
import storage

def evaluate (term, cmd):

	cmd = cmd.lower().split(" ")

	if (cmd[0] == "run"):

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

	else:

		term.addstr(f"Error: {cmd[0]} is not a valid option")

		return "err"
