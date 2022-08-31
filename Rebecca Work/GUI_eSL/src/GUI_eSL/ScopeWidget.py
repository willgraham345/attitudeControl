# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 18:17:38 2021

@author: Wintermute
"""


import numpy as np
import matplotlib.pyplot as plt
import sys
import pyvisa as visa
import datetime
from PyQt5.QtWidgets import QWidget
import math
import time
from oscilloscope import Oscilloscope
# from vispy.plot import Fig
from GUI_supporting_functions import datetimeToSeconds

class OscilloscopeWidget(QWidget):
    def __init__(self,this_widget=None,indicator=None,lbl=None,tied_device=None):
        super().__init__()
        self.this_widget= this_widget
        # Parse the buttons and inputs from the main GUI 
        self.ch1_lbl = this_widget[0]
        self.ch2_lbl = this_widget[1]
        self.ch3_lbl = this_widget[2]
        self.ch4_lbl = this_widget[3]
        
        self.run_btn = this_widget[4]
        
        self.ch1_range_in = this_widget[5]
        self.ch2_range_in = this_widget[6]
        self.ch3_range_in = this_widget[7]
        self.ch4_range_in = this_widget[8]
        self.range_set_btn = this_widget[9]
        self.offset_in = this_widget[10]
        self.offset_chan_sel = this_widget[11]
        self.offset_go_btn = this_widget[12]
        # connect buttons to functions
        self.offset_go_btn.clicked.connect(self.updateScopeOffset)
        self.range_set_btn.clicked.connect(self.updateScopeRange)

        # initialize variables
        self.tied_device = tied_device
        self.indicator = indicator
        self.lbl = lbl
        self.thread = None
        self.finished = False
        self.record = False
        self.scope = Oscilloscope()
        self.scope.AttachButton(self.run_btn)
        self.extra_info = ' '
        self.unit = 'V'
        # self.recorded_scope_data = []
        self.recorded_timestamps = []
        self.curr_timescale = None
        self.shunt_val = None
        self.num_channels = 4
        self.record_end_time = None
        
    def start(self):
        self.scope.Run()
        self.updateScopeRange()
        self.indicator.set_active(True)       
    def close(self):
        self.indicator.set_active(False)
        self.scope.Close()
    def clear(self):
        self.scope.Clear()
    def setTimeScale(self,scale):
        self.scope.SetTimescale(scale)
        # scope rounds up the timescale to nearest valid val
        self.curr_timescale = self.scope.GetTimescale()
    def getTimescale(self):
        return self.scope.GetTimescale()
    def startRecord(self):
        #ensure clean start
        self.clearRecord()
        self.record = True
        # self.scope.Run()
    def stopRecord(self):
        self.record = False 
        if self.scope.RUNNING:
            self.scope.Stop()
        self.record_end_time = datetimeToSeconds(datetime.datetime.now())
    def getRecording(self,channel,instrument): 
        data = self.scope.GetData(channel)
        print("data length: " + str(len(data)))
        self.createTimestamps(len(data))#self.recorded_timestamps = 
        return instrument,data, self.recorded_timestamps, self.unit, self.extra_info
    def clearRecord(self):
        self.recorded_timestamps = []
        # self.recorded_scope_data = []
        if not self.scope.RUNNING:
            self.scope.Run()
    def plotRecorded(self,supply_v,supply_ts,ttl,figpose=[0,0],channel_select=1,mode='cv'):
        # this functionality is rarely used, typically should use separate plotting 
        # functions
        # -----------
        # get the scope timestamps and convert to seconds, 
        # make equivalent Power supply voltage / timestamp list that can plot 
        # with the oscope data
        current_voltage_mode = 'cv'
        time_mode = 'time'
        scope_data = self.scope.GetData(channel_select)
        shunt_resistor = self.shunt_val * 1e6
        current = []
        scope_seconds = []
        if self.recorded_timestamps== []:
            self.createTimestamps(len(scope_data))
        scope_timestamps = self.recorded_timestamps
        scope_end_time = self.record_end_time
        full_supply_v = [0]*len(scope_timestamps) # init supply voltage list same size as scope data
        for i in range(len(scope_timestamps)):
            curr_scope_time = scope_timestamps[i]
            if mode == time_mode:
                elapsed_s = scope_end_time - curr_scope_time
                scope_seconds.append(elapsed_s)
            
            if mode == current_voltage_mode:
                # calculate the current value
                curr = scope_data[i] / shunt_resistor
                current.append(curr)
                # make voltage list same length as current list
                # ASSUMES THAT ALL TIME BEFORE RECORDING SUPPLY VOLTAGE IS 0
                for j in range(len(supply_ts)-1):
                    supply_time = float(supply_ts[j])
                    next_supply_time = float(supply_ts[j+1])
                    if (curr_scope_time >= supply_time) and (curr_scope_time < next_supply_time):
                        # found the voltage slot this scope reading fits into
                        full_supply_v[i] = supply_v[j]
                        break
        if mode == time_mode:
            plt.scatter(scope_seconds,scope_data)
            plt.ylabel('Voltage (V)')
            plt.xlabel('Time (S)')
        elif mode == current_voltage_mode:
            plt.scatter(full_supply_v,current)
            plt.ylabel('Current (A)')
            plt.xlabel('Voltage (V)') # note: power supply voltage not scope voltage
        plt.title(ttl)                        
        return plt
#    def tupleToSeconds(self,tup):
#        #convert to seconds
#        h = tup[0] * 60 *60 
#        m = tup[1] * 60
#        s = tup[2]
#        return h+m+s
        
    def createTimestamps(self,data_len):
        # the oscilloscope reports 3 million points, we know the time when the 
        # oscilloscope was stopped, and the time in between each datapoint. 
        # therefore, we can go backwards through the data and assign timestamps
        # to each datapoint retroactively.
        time_inc = self.scope.GetTimeIncrement() # seconds
        second = self.record_end_time
        timestamps = []
        for d in range(data_len):            
            timestamps.append(second)
            # update time for next loop
            second = second - time_inc
        # data came in with the most recent data first in the list-
        # for plotting purposes we want this to be reversed so that it is more 
        # in line with other recorded data files
        self.recorded_timestamps = np.flip(timestamps)
    def updateScopeRange(self):
        ch_settings = [self.ch1_range_in.text(),self.ch2_range_in.text(),self.ch3_range_in.text(),self.ch4_range_in.text()]
        for c in range(self.num_channels):
            chan = c + 1
            setting =  float(ch_settings[c]) * 8 # 8 virtical grid cells
            self.setVoltRange(chan, setting)
    def updateScopeOffset(self):
        desired_offset = float(self.offset_in.text())        
        chan = self.offset_chan_sel.currentText()
        if chan == 'ch1':
            chan = 1
        elif chan == 'ch2':
            chan = 2
        elif chan =='ch3':
            chan = 3
        elif chan == 'ch4':
            chan = 4
        self.scope.SetVerticalOffset(desired_offset, chan)
    def setVoltRange(self,channel,v_range):
        self.scope.SetVoltRange(channel, v_range)
    def activate(self):
        pass
    def setShuntR(self,r,r_unit):
        self.extra_info = str(r)+' '+r_unit
        self.shunt_val = r
    def Run(self):
        self.scope.Run()
    def Stop(self):
        self.scope.Stop()