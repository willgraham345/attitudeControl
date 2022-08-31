# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 17:01:03 2022

@author: Wintermute
"""
import sys
import pyvisa as visa
import numpy as np

class Oscilloscope():
    def __init__(self):
        rm = visa.ResourceManager()
        # Get the USB device, e.g. 'USB0::0x1AB1::0x0588::DS1ED141904883'
        instruments = rm.list_resources()
        usb = list(filter(lambda x: 'USB' in x, instruments))
        if len(usb) != 1:
            print('Bad instrument list', instruments)
            sys.exit(-1)
        self.scope = rm.open_resource(usb[0], timeout=500)#, chunk_size=1024000) # bigger timeout for long mem
        
        self.scope.write(":WAV:MODE RAW")
        self.scope.write(":WAV:FORM BYTE")
        self.RUNNING = None
        self.run_button = None
    def __debug_query__(self,cmd):
        return self.scope.query(cmd)
    def __debug_write__(self,cmd):
        self.scope.write(cmd)
    def AttachButton(self,btn):
        self.run_button = btn
    def Run(self):
        if not self.RUNNING:
            self.RUNNING = 1
            self.scope.write(":RUN")
        if self.run_button != None:
            self.run_button.setText("Stop")
            self.run_button.clicked.connect(self.Stop)
    def Stop(self):
        if self.RUNNING:
            self.RUNNING = 0
            self.scope.write(":STOP")
        if self.run_button != None:
            self.run_button.setText("Run")
            self.run_button.clicked.connect(self.Run)        
    def Close(self):
        self.scope.close()
    def Clear(self):
        self.scope.write(":CLEAR")
    def UpdateTimescale(self):
        self.timescale = float(self.scope.query(":TIM:SCAL?"))
    def GetTimescale(self):
        self.UpdateTimescale()
        return self.timescale 
    def SetTimescale(self,new_scale):
        # timescale value should be in seconds
        self.scope.write(":TIM:SCAL " + str(new_scale))
    def GetTimeIncrement(self):
        #returns the time increment in seconds
        return float(self.scope.query(":WAV:XINC?"))
    def GetData(self,channel,chunk_size=250000):
        # Grab the raw data from chosen channel
        self.Stop()
        self.scope.write(":WAV:SOUR CHAN"+str(channel))
        # Get the timescale
        self.timeinc = float(self.scope.query(":WAVeform:XINCrement?"))#float(scope.query(":TIM:SCAL?"))
        
        # Get the timescale offset
        self.timeoffset = float(self.scope.query(":TIM:OFFS?"))
        self.voltscale = float(self.scope.query(':CHAN'+str(channel)+':SCAL?'))
        
        # And the voltage offset
        self.voltoffset = float(self.scope.query(':CHAN'+str(channel)+':OFFSet?'))
        
        self.UpdateParams()
        
        rawdata = []
        sp = 1 # start at first point
        while len(rawdata) < self.num_points:
            diff = self.num_points - len(rawdata)
            if diff < chunk_size:
                ep = diff
            else:
                ep = sp + chunk_size - 1
            self.scope.write(":WAV:STAR "+str(sp))
            self.scope.write(":WAV:STOP "+str(ep))
            chunk = self.scope.query_binary_values(":WAV:DATA?",datatype='B')
            rawdata.extend(chunk)
            sp = sp + chunk_size       
        data_size = len(rawdata)
        raw_arr = np.array(rawdata)
        out_data = (raw_arr - self.yorigin - self.yref) * self.yinc
        return out_data
    def UpdateParams(self):
        # get header info - format,type,points,count,xincrement,xorigin,xreference,yincrement,yorigin,yreference
        header = self.scope.query(":WAV:PRE?")
        parsed = header.split(',')
        self.num_points = float(parsed[2])#the number of points on the scope
        self.xinc = float(parsed[4])
        self.xorigin = float(parsed[5])
        self.xref = float(parsed[6])
        self.yinc = float(parsed[7])
        self.yorigin = float(parsed[8])
        self.yref = float(parsed[9])
    def GetParams(self):
        return self.num_points,self.x_inc,self.xorigin,self.xref,self.yinc,self.yorigin,self.yref
    def SetVoltRange(self,channel,desired_range):
        cmd = ":CHANnel" + str(channel) + ":RANGe " + str(desired_range)
        self.scope.write(cmd)
    def SetVerticalOffset(self,offset,chan):
        if chan == 'all':
            num_chans = 4
            for i in range(num_chans):
                cmd = ':CHANnel'+str(i+1)+':OFFSet '+str(offset)
                self.scope.write(cmd)
        else:
            cmd = ':CHANnel'+str(chan)+':OFFSet '+str(offset)
    def SetDataLength(self,desired_length):
        #Sets the number of points that the oscilloscope will output when recording data
        pass        