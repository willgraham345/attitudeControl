# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 14:39:34 2022

@author: Wintermute
"""
from math import sqrt
# import time
import numpy as np
import serial


class xyStage():
    def __init__(self,serial_handle):
        self.ser = serial_handle#serial.Serial(serial_handle,115200)
        # self.ser.open()        
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        self.curr_x = 0
        self.curr_y = 0
        self.get_current_pos()
        
    def close(self):
        self.ser.close()    
    def go_to_steps(self,x,y):
        # X and Y are input as micometers, so 1000 is 1 mm, 10 is one notch, and 500 is one rotation.
        print(b'G00 X' + bytes(str(x), 'utf-8') + b' Y' + bytes(str(y), 'utf-8'))
        self.write(b'G00 X' + bytes(str(x), 'utf-8') + b' Y' + bytes(str(y), 'utf-8') + b'\n')
    
    
    # def find_zero(self):
    #     self.write(b'G91')
    #     print(self.ser.read(100))
    #     while(self.ser.is_open):
    #         y_or_n = input("Is the current position (0, 0)? (y/n): ")
    #         if y_or_n == "y":
    #             self.write(b'G90')
    #             self.ser.read(100)
    #             self.set_zero(self.ser)
    #             return
    #         elif y_or_n == "n":
    #             xval = input("Enter your delta x value (steps, 64 should be 1 notch): ")
    #             yval = input("Enter your delta y value (steps, 64 should be 1 notch): ")
    #             self.go_to_steps(self.ser, int(xval), int(yval))
    #         else:
    #             print('Input not understood. Try \'y\' or \'n\'.')
    
    
    def set_zero(self):
        self.write(b'G92 X0\n')
        self.write(b'G92 Y0\n')
    
    
    def go_to(self,x,y):
        # X and Y are input as micrometers, so 1000 is 1 mm, 10 is one notch, and 500 is one rotation.
        # https://www.desmos.com/calculator/1ndnxhucyv
        xsteps = (x*(1e-3))
        ysteps = (y*(1e-3))
        # Debugging info, prints GCode
        # print(b'G00 X' + bytes(str(xsteps), 'utf-8') + b' Y' + bytes(str(ysteps), 'utf-8'))

        self.write(b'G00 X' + bytes(str(xsteps), 'utf-8') + b' Y' + bytes(str(ysteps), 'utf-8') + b'\n')


    def is_idle(self):
        self.write(b'?')
        line = self.ser.read_until()
        line.strip()
        parsed_line = line.split(b',')
        #print(parsed_line)
        if len(parsed_line) > 1:
            status = parsed_line[0]
            if(status == b'<Idle'):
                return True
            elif status == b'<Run':
                return False
            else:
                re_parsed = status.split(b'<')
                if re_parsed[1] == b'Idle':
                    return True
                elif re_parsed[1] == b'Run':
                    return False
                else:
                    print("Error measuring idle. Debug \is_idle()\ got '" + str(status) + "'" )
                    return
        else:
            return False
        
    def write(self,msg):
        self.ser.flush()
        self.ser.write(msg)
        
    def get_current_pos(self):
        self.write(b'?')
        line = self.ser.read_until()
        line.strip()
        halved_line = line.split(b':')
        if len(halved_line) == 3:
            work_pose = halved_line[2]
            wp_stripped = work_pose.split(b'>')
            xyz_coords = wp_stripped[0]
            parsed_coords = xyz_coords.split(b',')
            x = parsed_coords[0]
            y = parsed_coords[1]
            self.curr_x = float(x)*(1e3)#mm to micrometer
            self.curr_y = float(y)*(1e3)
            
        return (self.curr_x,self.curr_y)# output in micrometer
    
    