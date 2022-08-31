# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 16:40:30 2021

@author: Becca
"""
# from zaber.serial import AsciiSerial, AsciiCommand
from PyQt5.QtWidgets import QWidget
from SensorProcessing import Worker
from PyQt5.QtCore import QTimer
import serial        
import numpy as np
import datetime
import matplotlib.pyplot as plt



def datetimeToSeconds(t):
    h = t.hour * 3600
    m = t.minute * 60
    s = t.second + (t.microsecond*1e-6)
    return h+m+s

class Element():
    def __init__(self, this_widget=None, tied_device=None):
        self.this_widget = this_widget
        self.tied_device = tied_device
        self.thread      = None
        self.extra_info  = ''
    def start(self):
        for w in self.this_widget:
            w.show()
        
class ForceSensorWidget(QWidget):
    def __init__(self,this_widget=None,indicator=None,lbl=None,tied_device=None):
        super().__init__()
        self.this_widget= this_widget
        self.indicator = indicator
        self.lbl = lbl
        self.tied_device = tied_device
        self.thread = None
        self.force_timer = None
        self.recorded_data = np.array([])
        self.recorded_timestamps = np.array([])
        self.record = False
        self.unit = 'N'
        self.extra_info = ' '
    def start(self):
        if self.tied_device is not None: 
            self.tied_device.data = 0
            #Serial initialization
            com = self.tied_device.serial_port
            self.port = serial.Serial(com,timeout=0.05,baudrate=115200)#AsciiSerial(com,timeout=0.05)
            self.tied_device.port = self.port
            #Start thread to collect data
            self.thread = Worker(self)
            self.thread.check_info = self.check_info
            self.thread.data.connect(self.onDataFromThread)
            self.thread.start()
            #Start timer to update display
            self.force_timer = QTimer(self)
            self.force_timer.setInterval(50) #Update display every 50 mS
            self.force_timer.timeout.connect(self.updateDisplay)
            self.force_timer.start()
            self.new_data_available = False
            
            self.indicator.set_active(True)
    def close(self):
        if self.thread != None:
            self.thread.stop()
        if self.force_timer != None:
            self.force_timer.stop()
        if self.port != None:
            self.port.close()
        self.indicator.set_active(False)
        print('Closed Force Sensor')
    def startRecord(self):
        # n = datetime.datetime.now()
        # print('started force sensor record at ' + str(n.time()))
        self.record = True
    def stopRecord(self):
        self.record = False
    def getRecording(self):
        return self.lbl,self.recorded_data, self.recorded_timestamps, self.unit, self.extra_info
    def clearRecord(self):
        self.recorded_data = []
        self.recorded_timestamps = []
    def plotRecorded(self,v,v_ts,ttl):
        mapped_v = [0]*len(self.recorded_data)
        for i in range(len(self.recorded_timestamps)):
            f_ts = float(self.recorded_timestamps[i])
            idx = None
            for j in range(len(v)):
                supply_ts = float(v_ts[j])
                if supply_ts <= f_ts:
                    idx = j
                else:
                    break 
            if idx is None: # if the silly scope started before the power supply, assume the power supply starts off
                mapped_v[i] = 0
            else:
                mapped_v[i] = v[idx]
        plt.scatter(mapped_v,self.recorded_data)
        plt.ylabel('Force ('+self.unit+')')
        plt.xlabel('Voltage (V)')
        plt.title(ttl)
        return plt
    def activate(self):
        pass
    def onDataFromThread(self, msg):
        if msg != '':
            self.tied_device.data = float(msg)
            if self.record:
                if self.new_data_available:
                    t = datetime.datetime.now()
                    self.recorded_data = np.append(self.recorded_data,float(msg))
                    self.recorded_timestamps = np.append(self.recorded_timestamps,str(datetimeToSeconds(t)))
                    
                    self.new_data_available = False
    def updateDisplay(self):
        full_txt = 'Force Data: ' + str(round(self.tied_device.data,5)) + ' ' +self.unit
        self.this_widget.setText(full_txt)
    def check_info(self):
        try:
            command = bytearray('!001:SYS?\r',encoding='ascii')
            self.port.write(command)
            reply = self.port.read_until('\r')
            self.new_data_available = True
                    # if self.record:
                    #     a = datetime.datetime.now()
                    #     print(a.time())
            if reply != '':
                msg = str(float(reply)) #admittedly not particularly efficient (bytes->float->str->float)
                #if everything is working properly, indicator should say so
            if not self.indicator.get_active(): 
                self.indicator.set_active(True)
            return msg
        except:
            #if something goes wrong, or port closes unexpectedly, indicate connection lost
            if self.indicator.get_active(): 
                self.indicator.set_active(False)
            pass

class AnemometerWidget(QWidget):
    def __init__(self,this_widget=None,indicator=None,lbl=None,tied_device=None):
        super().__init__()
        self.this_widget= this_widget
        self.indicator= indicator
        self.lbl = lbl
        self.tied_device = tied_device
        self.thread = None
        self.unit_parse = {
            '01' : 'C',
            '02' : 'F',
            '08' : 'm/S',
            '09' : 'Knot',
            '10' : 'Km/h',
            '11' : 'ft/min',
            '12' : 'mph',
            '84' : 'CMM',
            '85' : 'CFM'
            }
        
        self.curr_velocity = ''
        self.curr_temp    = ''
        self.v_unit = ''
        self.t_unit = ''
        self.recorded_vel = []
        self.recorded_vel_unit =  []
        self.recorded_temp =  []
        self.recorded_temp_unit =  []
        self.recorded_timestamps = []
        self.record = False
        self.anem_timer = None
        self.new_data_available = False
        
    def start(self):
        if self.tied_device is not None:      
            com = self.tied_device.serial_port
            self.port = serial.Serial(com,timeout=1,baudrate=9600,parity=serial.PARITY_NONE)
            self.port.flush()
            self.tied_device.port = self.port
            #Start thread to collect data
            self.thread = Worker(self)
            self.thread.check_info = self.check_info
            self.thread.data.connect(self.onDataFromThread)
            self.thread.start()
            #Start timer to update display
            self.anem_timer = QTimer(self)
            self.anem_timer.setInterval(50) #Update display every 50 mS
            self.anem_timer.timeout.connect(self.updateDisplay)
            self.anem_timer.start()
            
            self.indicator.set_active(True)
    def close(self):
        if self.thread != None:
            self.thread.stop()
        if self.anem_timer != None:
            self.anem_timer.stop()
        if self.port != None:
            self.port.close()
        self.indicator.set_active(False)
        print('Closed Anemometer')
        
    def activate(self):
        pass
    def startRecord(self):
        # n = datetime.datetime.now()
        # print('started anemometer record at ' + str(n.time()))
        self.record = True
    def stopRecord(self):
        self.record = False
    def getRecording(self):
        # avg_temp = str(np.mean(self.recorded_temp)) + self.recorded_temp_unit[-1]
        if len(self.recorded_temp)>0:
            ei = str(np.mean(self.recorded_temp)) + ' ' + self.recorded_temp_unit[0]
            return self.lbl+' velocity',self.recorded_vel, self.recorded_timestamps, self.recorded_vel_unit[-1], ei
        else:
            return self.lbl+' velocity', [' '], [' '], ' ', ' '
    def clearRecord(self):
        self.recorded_vel = []
        self.recorded_vel_unit =  []
        self.recorded_temp =  []
        self.recorded_temp_unit =  []
        self.recorded_timestamps = []
    def plotRecorded(self,v,v_ts,ttl):
        mapped_v = [0]*len(self.recorded_vel)
        for i in range(len(self.recorded_timestamps)):
            ane_ts = float(self.recorded_timestamps[i])
            idx = None
            for j in range(len(v)):
                silly_scope_ts = float(v_ts[j])
                if silly_scope_ts <= ane_ts:
                    idx = j
                else:
                    break 
            if idx is None: # if the silly scope started before the power supply, assume the power supply starts off
                mapped_v[i] = 0
            else:
                mapped_v[i] = v[idx]
        plt.scatter(mapped_v,self.recorded_vel)
        plt.ylabel('Velocity ('+self.recorded_vel_unit[-1]+')')
        plt.xlabel('Voltage (V)')
        plt.title(ttl)
        return plt
    def updateDisplay(self):
        msg_l1 = 'Velocity: ' + str(self.curr_velocity) + ' ' + self.v_unit 
        msg_l2 = 'Temperature: ' + str(self.curr_temp)  + ' ' + self.t_unit
        full_txt = msg_l1 + '\n' + msg_l2
        self.this_widget.setText(full_txt)
    def splitString(self,word):
        return [char for char in word]
    def list2String(self,s):
        out = ''
        for e in s:
            out = out + e
        return out
    def onDataFromThread(self, msg):
        msg_tup = msg.split(',')
        try:
            v = float(msg_tup[0])
            t = float(msg_tup[1])
            v_unit = msg_tup[2]
            t_unit = msg_tup[3]
            self.tied_device.data = [v,t]
            self.units = [v_unit,t_unit]
            self.curr_temp = t
            self.curr_velocity = v
            self.v_unit = v_unit
            self.t_unit = t_unit
            if self.record and self.new_data_available:
                n = datetime.datetime.now()
                self.recorded_vel.append(v)
                self.recorded_vel_unit.append(v_unit)
                self.recorded_temp.append(t)
                self.recorded_temp_unit.append(t_unit)
                self.recorded_timestamps.append(str(datetimeToSeconds(n)))
                self.new_data_available = False
                # print('added anemometer ts ' + str(n.time()))
            if not self.indicator.get_active(): # if something went wrong, retry serial port
                if self.port.isOpen():
                    self.port.flush()
                else:
                    com = self.tied_device.serial_port
                    self.port = serial.Serial(com,timeout=1,baudrate=9600,parity=serial.PARITY_NONE)
                    self.port.flush()
                    self.tied_device.port = self.port
        except:
            self.indicator.set_active(False)
            if self.port.isOpen():
                self.port.flush()
    def check_info(self):
        '''
        sort incoming data into velocity and temperature readings
        '''
        for k in range(2): # data comes in pairs, first velocity, then temp
            data,unit,isVelocity = self.readData()
            if self.indicator.get_active():
                if isVelocity:
                    v = str(data)
                    v_unit = self.unit_parse[unit]
                else:
                    t = str(data)
                    t_unit = self.unit_parse[unit]
                    v = 'None'
                    v_unit = 'None'
        
        self.new_data_available = True
        #if everything is working properly, indicator should say so
#            if not self.indicator.get_active(): 
        if self.indicator.get_active():
            msg = v + ',' + t + ',' + v_unit +',' + t_unit
            return msg  
    def readData(self):
        '''
        Get data from Anemometer device
        Format:
            D15 ... D0 
            D0 - End word 
            D1&D8 - Display reading, D1= LSD, D8 MSD
            D9 - decimal point position from right to left 
               0 = no DP, 1 = 1 DP, 2 = 2 DP, 3 = 3 DP
            D10 - Polarity (0 = Positive, 1 = negative)
            D11&12 Annunciator for Display (unit)
                degrees C = 01
                degrees F = 02
                m/S = 08
                Knot = 09
                Km/h = 10
                ft/min = 11
                mile/h = 12
                CMM = 84
                CFM = 85
            D13 - upper display data = 1, lower display data = 2
            D14 - 4
            D15 - start word
        '''
        try:
            self.port.flush()
            raw_reply = self.port.read(16)
            decoded_reply = raw_reply.decode() # convert to str
            segmented_reply = self.splitString(decoded_reply)
            data = float(self.list2String(segmented_reply[7:])) # 8 bytes of data
            dec_loc = int(self.list2String(segmented_reply[6]))
            unit_code =  self.list2String(segmented_reply[3:5])
            isVelocity =  self.list2String(segmented_reply[2])=='1'
            if dec_loc > 0:
                scaled_data = (data)/(10**(dec_loc))
            else:
                scaled_data = data
            self.indicator.set_active(True)
            return scaled_data,unit_code,isVelocity
        except:
            self.indicator.set_active(False)
            return None,None,None
        
        