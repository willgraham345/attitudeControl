# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 16:56:51 2022

@author: Wintermute
"""
import socket

class SpellmanHVSupply():
    def __init__(self):
        # init variables
        self.curr_kv = None
        self.curr_mA = None
        # set up communication
        self.ip_addr = '192.168.10.61'
        self.port_addr = 50001
        self.ip_buffer_size = 1024
        self.com = None
        self.openComm()
     
    def openComm(self):
        # open communication
        self.com = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.com.settimeout(5)
        self.com.connect((self.ip_addr, self.port_addr))
        
    def closeComm(self):
        # shut down communication
        self.com.close()
        self.com = None
        
    def sendCmd(self,cmd):
        # Formats message and sends to supply
        self.reply = None
        msg_string = '\x02'+cmd+',\x03'
        msg_out = msg_string.encode('ascii')
        print('sending: ' + str(msg_out))
        self.com.send(msg_out)
        try: # ensure message was recieved 
            self.reply = self.receiveResponse()
        except:
            print('No response from supply')
            
    def receiveResponse(self):
        # receive, decode and parse response received from supply.
        data = self.com.recv(2048)
        decoded_data = data.decode('ascii')
        print('received: ' + str(decoded_data))
        parts = str(decoded_data).split(',') #parse response
        response = parts[1:-1] #cut off start and end bytes
        if len(response) == 1:
            return response[0]
        elif len(response) > 1:
            return response
        else:
            raise ValueError('invalid response received from HV supply')
            
    def getReply(self):
        # report on the most recent message sent from the power supply.
        return self.reply
    
    def HVOutput(self,toggle_on):
        # turn on or off HV output
        if toggle_on:
            # HV ON
            self.sendCmd('99') # 99 = on command for HV supply
        else:
            # HV OFF
            self.sendCmd('98') # 98 = off command for HV supply

    def setKV(self,desired_kV):
        # takes in kV voltage format
        # convert voltage to command, set desired kV value
        # note: new HV supply -> 0-10kV, 0 min, 4095 max
        max_kV = 10
        if (desired_kV >= 0) and (desired_kV <= max_kV):
            max_vout = max_kV * 1e3 #V
            voltage = desired_kV * 1e3
            cmd_vout = (4095*voltage) / max_vout
            cmd = '10,'+str(int(cmd_vout))
            self.sendCmd(cmd)
        else:
            raise ValueError('Invalid Voltage Requested')
        
    def setmA(self,desired_mA):  
        # takes in mA current format
        # convert mA current to command, set desired mA value
        # note: new HV supply -> 0-3mA, 0 min, 4095 max
        max_mA = 3
        if (desired_mA >= 0) and (desired_mA <= max_mA):
            cmd_Iout = (4095*desired_mA) / max_mA
            cmd = '11,'+str(int(cmd_Iout))
            self.sendCmd(cmd)
        else:
            raise ValueError('Invalid Current Requested')
        
    def getkV(self):
        # Returns current voltage setpoint in kV
        self.sendCmd('14')
        raw_reply = float(self.reply)
        kV = (10*raw_reply) / 4095
        return kV
        
    def getmA(self):
        # Returns current current setpoint in mA
        self.sendCmd('15')
        raw_reply = float(self.reply)
        mA = (3*raw_reply) / 4095
        return mA
    
    def HVStatus(self):
        # returns 1 if HV is ON, 0 if HV is OFF
        self.sendCmd('22')
        return int(self.reply)
    
    def systemStatus(self):
        # report faults and status messages
        status_decoded = ['Interlock closed','HV inhibited','Over voltage', 
                          'Over current', 'Over power','Regulator error',
                          'Arc fault', 'Over temperature','Adjustable overload',
                          'System fault', 'Remote mode']
        
        self.sendCmd('32')
        status_msg = self.reply
        for i in range(len(status_msg)):
            status = int(status_msg[i])
            if status:
                print(status_decoded[i])
            else: # interlock and mode messages have 2 options, print 0 case message.
                if i == 0:
                    print('Interlock open')
                elif i == 10:
                    print('Local mode')
    
    def clearFaults(self):
        # reset faults
        self.sendCmd('52')
        
    def getADCData(self):
        self.sendCmd('20')
        raw_reply = self.reply
        self.curr_kv = ((float(self.reply[0]) + -1*float(self.reply[8]))*10)/3983
        self.curr_mA = (float(self.reply[1])*3)/3983
        
    def getKVReading(self):
       self.getADCData()
       return self.curr_kv
   
    def getmAReading(self):
       self.getADCData()
       return self.curr_mA
        
        