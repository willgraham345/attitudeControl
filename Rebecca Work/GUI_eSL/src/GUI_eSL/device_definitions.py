# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 17:06:18 2021

@author: Wintermute
"""
class Device:
    def __init__(self, serial_num, device_id):
        self.serial_num  = serial_num
        self.device_id   = device_id
        self.serial_port = 'COM1' 
        self.port        = None
        self.data        = None
        self.hdwf        = None
        self.sts         = None
    def setCOM(self,com_port):
        self.serial_port = com_port
    def updateData(self,new_data):
        self.data = new_data
  