import socket
import time
import traceback
import cv2
import numpy as np
import threading
from sys import exit


#global data img
data = 0;

# server side handler
is_relaying = False
cli_address = ('', 0)
host = ''
port = 10219
ser_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ser_socket.bind((host, port))

# Client
IPDICT = {}



#CLIENT SIDE		
ser_address = ('192.168.1.156', 10218)
cli_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cli_socket.settimeout(5)
class UdpReceiver(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.thread_stop = False
                
	def run(self):
		while not self.thread_stop:
			global cli_address
			global is_relaying
			try:
				message, address = ser_socket.recvfrom(65536)
				cli_address = address
			except:
				traceback.print_exc()
				continue
			print cli_address
			if message == 'startRealy':
				print 'startRealy'
				is_relaying = True
				print cli_address[0]
				IPDICT[cli_address[0]] = cli_address[1]			
				ser_socket.sendto('startRcv', cli_address)                
			if message == 'quitCam':
				is_relaying = False
				del IPDICT[cli_address[0]]
				cli_socket.sendto('quitCam', ser_address)
				cli_socket.close()
				receiveThread.stop()
				ser_socket.close()
				print 'quit camera'
				exit()	
	def stop(self):
		self.thread_stop = True

receiveThread = UdpReceiver()
receiveThread.setDaemon(True)        
receiveThread.start()		
		

while 1:
    cli_socket.sendto('startCam', ser_address)
    try:
        message, address = cli_socket.recvfrom(65536)
        if message == 'startRcv':
            print message
            break
    except socket.timeout:
        continue
while 1:
	if message == 'quitCam':
		break
	try:
		data, address = cli_socket.recvfrom(65536)
	except socket.timeout:
		continue
	if is_relaying or len(IPDICT) > 0:		
		for keys,values in IPDICT.items():
			ser_address = (keys, values)
			ser_socket.sendto(data, ser_address) 
		time.sleep(0.05)
	else:
		time.sleep(1)		


