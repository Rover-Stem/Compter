import time
import queue
import socket
import storage
import threading

class client ():

	def __init__ (self, testing, host, port, packetSize):

		self.__host = host
		self.__port = port
		self.__sockt = socket.socket()
		self.__testing = testing
		self.__outgoing = queue.Queue(maxsize = 10)
		self.__incoming = queue.Queue(maxsize = 50)
		self.__packetSize = packetSize

		if (testing):

			self.__host = "127.0.0.1"

		while True:

			try:

				self.__sockt = socket.socket()
				self.__sockt.connect((socket.gethostbyname(self.__host), self.__port))

				storage.connected = True

				print("Connected!") # Use as animation end trigger

				break

			except:

				if (storage.exit):

					break

	def cleanUp (self):

		self.__sockt.shutdown(SHUT_RDWR)

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

				for i in str(data, 'utf-8').split(",:f\5~"):

					with open("log.txt", 'a') as f:

						f.write(f"Added {i} to incoming messags\n\n")

					storage.messagesIn.put(i)

					if (i == "stop"):

						self.cleanUp()

						break

			data = None

	def sendMessages (self, conn):

		if (self.__testing):

			conn.send(bytes("T", 'utf-8'))

		else:

			conn.send(bytes("NT", 'utf-8'))

		while (True):

			if not(storage.messagesOut.empty()):

				msg = bytes(storage.messagesOut.get(), 'utf-8')

				with open("log.txt", 'a') as f:

					f.write(f"Added {str(msg, 'utf-8')} to outgoing messags\n\n")

				conn.send(bytes(str(msg, 'utf-8') + ",:f\5~", 'utf-8'))

				if (str(msg, 'utf-8') == "stop"):

					break