import queue
import storage
from terminal import safeScroll

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

		return "end"

	else:

		term.addstr(f"Error: {cmd[0]} is not a valid option")
		safeScroll(term)

		return "err"
