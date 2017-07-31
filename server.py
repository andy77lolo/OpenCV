import socket
import time
import traceback
import cv2
import numpy as np
import threading
from sys import exit

# cv2 init
camera = cv2.VideoCapture(0)
camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 160); 
camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 120);
camera.set(cv2.cv.CV_CAP_PROP_SATURATION,0.2);


# server side handler
is_sending = False
cli_address = ('', 0)
host = ''
port = 10218
ser_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ser_socket.bind((host, port))


# Client
IPDICT = {}

class UdpReceiver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_stop = False
                
    def run(self):
        while not self.thread_stop:
            global cli_address
            global is_sending
            try:
                message, address = ser_socket.recvfrom(4096)
                cli_address = address
            except:
                traceback.print_exc()
                continue
       #     print message,cli_address
            print cli_address
            if message == 'startCam':
                print 'start camera'
                is_sending = True
                print cli_address[0]
                IPDICT[cli_address[0]] = cli_address[1]			
                ser_socket.sendto('startRcv', cli_address)                
            if message == 'quitCam':
                is_sending = False
                del IPDICT[cli_address[0]]				
                print 'quit camera',

    def stop(self):
        self.thread_stop = True


receiveThread = UdpReceiver()
receiveThread.setDaemon(True)        
receiveThread.start()

while 1:
	if is_sending or len(IPDICT) > 0 :      
		#img = cam.getImage().resize((160,120))
		f,img = camera.read()
		data = img
		for keys,values in IPDICT.items():
			ser_address = (keys, values)
			ser_socket.sendto(data, ser_address) 
		time.sleep(0.05)
	else:
		time.sleep(1)

receiveThread.stop()
ser_socket.close()
