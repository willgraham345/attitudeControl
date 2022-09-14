# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 12:03:38 2022

@author: Wintermute
"""


import serial
import serial.tools.list_ports
import time

class arduinoControl():
    def __init__(self, port, baudrate):
        self.availablePorts = serial.tools.list_ports.comports()
        try:
            self.arduino = serial.Serial(
                port=port,
                baudrate=baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
            print('success connecting to arduino')
        except SerialException:
            print('error connecting to arduino')

    def write_pwm(self,pwmInput):
        self.arduino.write(bytes(pwmInput, 'utf-8'))

    def read_Arduino(self):
        msg = self.arduino.readline()
        return msg
      