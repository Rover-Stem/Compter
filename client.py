import time
import queue
import socket
import storage
import threading

class client ():

	def __init__ (self, host = socket.gethostbyname("raspberrypi.local"), port = 29500, packetSize = 1024):

		self.__host = host
		self.__port = port
		self.__packetSize = packetSize
		self.__sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.__outgoing = queue.Queue(maxsize = 10)
		self.__incoming = queue.Queue(maxsize = 50)

		while True:

			try:

				self.__sockt.connect((host, port))

				print("Connected!") # Use as animation end trigger

				break

			except:

				pass

	def cleanUp (self):

		self.__sockt.shutdown(__sockt.SHUT_RDWR)

		self.__sockt.close()

		print("Connection Closed") # Add goodbye message

	def run (self):

		tRecv = threading.Thread(target = self.receiveMessages, args = [self.__sockt], daemon = True)
		tRecv.start()

		tSend = threading.Thread(target = self.sendMessages, args = [self.__sockt], daemon = True)
		tSend.start()

	def receiveMessages (self, conn):

		data = None

		while (True):

			data = conn.recv(self.__packetSize)

			if data:

				if (str(data, 'utf-8') == "file"):

					filename = str(conn.recv(self.__packetSize), 'utf-8')

					with open(f"./images/{filename}", "wb") as f:

						while True:

							bytes_read = client_socket.recv(self.__packetSize)

							if not bytes_read:

								break

							f.write(bytes_read)

					storage.messagesIn.put(f"S,File {filename} Recieved")

				else:

					storage.messagesIn.put(str(data, 'utf-8'))

					if (str(data, 'utf-8') == "stop"):

						self.cleanUp()

						break

		data = None

	def sendMessages (self, conn):

		while (True):

			if not(storage.messagesOut.empty()):

				msg = bytes(storage.messagesOut.get(), 'utf-8')

				conn.send(msg)

				if (str(msg, 'utf-8') == "stop"):

					break