import socket, time
import pygame
from pygame.locals import *
from sys import exit
ser_address = ('192.168.1.116', 10219)
cli_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cli_socket.settimeout(5)
while 1:
    cli_socket.sendto('startRealy', ser_address)
    try:
        message, address = cli_socket.recvfrom(2048)
        if message == 'startRcv':
            print message
            break
    except socket.timeout:
        continue
cli_socket.recvfrom(65536)
pygame.init()
screen = pygame.display.set_mode((160,120))
pygame.display.set_caption('Web Camera1')
pygame.display.flip()
clock = pygame.time.Clock()
while 1:
    try:
        data, address = cli_socket.recvfrom(65536)
    except socket.timeout:
        continue
    camshot = pygame.image.frombuffer(data, (160,120), 'RGB')
    camshot = pygame.transform.scale(camshot, (160, 120))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
			print "quit"
			cli_socket.sendto('quitCam', ser_address)
			cli_socket.close()
			pygame.quit()
			exit()
    screen.blit(camshot, (0,0))
    pygame.display.update() 
    clock.tick(20)
