import queue
import threading

messagesIn = queue.Queue(maxsize = 50)
messagesOut = queue.Queue(maxsize = 10)

exit = False
connected = False

devicesIP = []
devicesARP = []
devicesDNS = []
devicesBluetooth = []