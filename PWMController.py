# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 12:03:38 2022

@author: Wintermute
"""


import serial


class PWMController():
    def __init__(self,serial_handle):
        self.ser = serial_handle
    
    def close(self): 
        self.setPWM(100)
        self.ser.close()
        
    def setPWM(self,pwm):
        msg = bytearray([pwm])
        self.ser.write(msg)
        
      