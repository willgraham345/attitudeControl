# -*- coding: utf-8 -*-
"""
Created on Thu May 12 11:16:14 2022

@author: Wintermute
"""

import socket

# Prepare 3-byte control message for transmission
TCP_IP = '192.168.10.61'
TCP_PORT = 50001
BUFFER_SIZE = 1
msg = '\x02'+str(99)+',\x03'#.encode('ascii') # Relays 1 permanent off
MESSAGE = msg.encode('ascii') 

# Open socket, send message, close socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)#bytes('','ascii'))
# s.sendmsg([msg])
#s.send(MESSAGE)   
try:
    data =  s.recv(1024) #s.recv(BUFFER_SIZE).decode('ascii')
    print(data.decode('ascii'))
except:
    print('No response from supply')
s.close()