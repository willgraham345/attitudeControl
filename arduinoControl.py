# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 12:03:38 2022

@author: Wintermute
"""


import serial
import time

class arduinoControl(port, baudrate, timeout):
    def __init__(self):
        self.serialObj  = serial.Serial(port = portGiven, baudrate, timeout)
    
    def (self):
        self.setPWM(100)
        self.ser.close()
        
    def setPWM(self,pwm):
        msg = bytearray([pwm])
        self.ser.write(msg)
        
      