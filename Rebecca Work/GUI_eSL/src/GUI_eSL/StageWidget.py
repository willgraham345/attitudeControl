# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 14:11:11 2022

@author: Wintermute
"""
import numpy as np
import datetime
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit, QLabel, QSpacerItem
from PyQt5.QtGui import QIntValidator, QFont
from PyQt5.QtCore import QSize, QTimer, Qt
from GUI_supporting_functions import datetimeToSeconds
from xystage import xyStage
import serial
from math import sqrt

class XYStageWidget(QWidget):
    def __init__(self,this_widget=None,indicator=None,lbl=None,tied_device=None):
        super().__init__()
        self.this_widget= this_widget
        self.indicator = indicator
        self.lbl = lbl
        self.tied_device = tied_device
        self.thread = None
        self.port = None
        self.recorded_data = []
        self.recorded_timestamps = []
        self.record = False
        self.unit = 'micrometer'
        self.extra_info = ' '
        self.stage = None
        self.calibrate_btn = None
        self.is_calibrating = False
        self.curr_x = 0
        self.curr_y = 0
        self.curr_goal = (0,0)
        self.move_timer = None
        self.display_timer = None
        self.pointlist = []
        self.RUN_CONTINUOUS = False
        self.pause_timer = None
        self.paused = False
        self.endTimer = None
        self.xmin = 0
        self.xmax = 10000
        self.ymin = 0
        self.ymax = 10000
        # self.postExperimentHoming = False
        
    def start(self):
        if self.tied_device is not None:    
            com = self.tied_device.serial_port
            self.port = serial.Serial(com,115200,timeout=1)
            self.tied_device.port = self.port
            self.stage = xyStage(self.port)
            self.calibrate_btn = self.this_widget[0]
            self.num_samples = self.this_widget[1]
            self.shape_select = self.this_widget[2]
            # self.size_input = self.this_widget[3]
            self.shape_execute_btn = self.this_widget[3]
            self.x_input = self.this_widget[4]
            self.y_input = self.this_widget[5]
            self.go_to_btn = self.this_widget[6]
            self.go_home_btn = self.this_widget[7]
            self.record_run_toggle = self.this_widget[8]
            self.pose_display = self.this_widget[9]
            # self.size_min = self.this_widget[11]
            self.x_min_input = self.this_widget[10]
            self.x_max_input = self.this_widget[11]
            self.y_min_input = self.this_widget[12]
            self.y_max_input = self.this_widget[13]
            self.x_min_lbl = self.this_widget[14]
            self.x_max_lbl = self.this_widget[15]
            
            self.shape_select.currentIndexChanged.connect(self.updateInputBoxes)
            self.go_home_btn.clicked.connect(self.handleGoHome)
            self.go_to_btn.clicked.connect(self.handleGoBtn)
            self.shape_execute_btn.clicked.connect(self.handleShapeExecute)
            self.createPopUp()
            self.calibrate_btn.clicked.connect(self.showPopUp)
            
            #create the timer if not already there (i.e. executing the first point in the list
            if self.display_timer == None:
                self.display_timer = QTimer(self)
                self.display_timer.setInterval(500) # 1 mS
                self.display_timer.timeout.connect(self.updatePoseDisplay)
            self.display_timer.start()

            self.indicator.set_active(True)
            
    def close(self):
        if self.stage != None:
            self.stage.close()
        if self.move_timer != None:
            self.move_timer.stop()
        if self.display_timer != None:
            self.display_timer.stop()
        if self.pause_timer != None: 
            self.pause_timer.stop()
        self.indicator.set_active(False)
        print('Closed XY Stage')
    def handleGoHome(self):
        # self.pointlist = [(0,0)]
        # self.beginPointListExecution()
        self.moveStage((0,0))
    def handleGoBtn(self):
        self.pointlist = []
        desired_x = float(self.x_input.text())
        desired_y = float(self.y_input.text())
        self.pointlist.append((desired_x,desired_y))
        self.beginPointListExecution()
    def handleShapeExecute(self):
        # l = float(self.size_input.text())
        self.xmin = float(self.x_min_input.text())
        self.xmax = float(self.x_max_input.text())
        self.ymin = float(self.y_min_input.text())
        self.ymax = float(self.y_max_input.text())
        s = self.shape_select.currentText()
        n = int(self.num_samples.text())
        # print('finished step 2:handle shape execute')
        self.go_to_points(n,shape=s)
    def handleEndCal(self):
        self.calibrate()
        self.endTimer.stop()
    def updatePoseDisplay(self):
        if (self.port != None) and (self.port.isOpen()):
            pose = self.stage.get_current_pos()
            self.curr_x = pose[0]
            self.curr_y = pose[1]
            txt = 'Curr Pose: (' + str(self.curr_x) + ', ' + str(self.curr_y) + ')'
            self.pose_display.setText(txt)
    def createPopUp(self):
        self.window = QWidget()
        self.layout = QGridLayout()
        self.window.setMinimumSize(QSize(500,100)) 
        self.window.setWindowTitle("Calibrate XY Stage") 
        self.window.setLayout(self.layout)
        spacer_item = QSpacerItem(1, 1) 
        lbl_font = QFont('Arial',10)
        inquiry = QLabel('Please Enter the Current Position Reading in Micrometers') 
        inquiry.setFont(lbl_font)
        x_lbl = QLabel('X:')
        y_lbl = QLabel('Y:')
        
        self.x_cal_input = QLineEdit('0')
        self.y_cal_input = QLineEdit('0')
        
        x_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        y_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.x_cal_input.setValidator(QIntValidator())
        self.y_cal_input.setValidator(QIntValidator())
        
        self.ok_btn = QPushButton("Ok")
        self.ok_btn.clicked.connect(self.calibrate)
        
        self.layout.addWidget(inquiry,0,0,1,5)
        self.layout.addWidget(x_lbl , 1,0,1,1)
        self.layout.addWidget(self.x_cal_input,1,1,1,1)
        self.layout.addItem(spacer_item,1,2,1,1)
        self.layout.addWidget(y_lbl, 1,3,1,1)
        self.layout.addWidget(self.y_cal_input,1,4,1,1)
        self.layout.addWidget(self.ok_btn,2,4,1,1)
        
        self.window.hide()
    def showPopUp(self):
        # ensure that the calibration starts clean, motors are sometimes confused at startup,
        # also allows you to not need to calibrate if stage is already at 0,0
        self.stage.set_zero()
        self.window.show()
    def closeWindow(self):
        self.window.hide()  
    def calibrate(self):
        self.is_calibrating = True
        self.curr_x = float(self.x_cal_input.text())
        self.curr_y = float(self.y_cal_input.text())
        self.x_cal_input.setText('0')
        self.y_cal_input.setText('0')
        self.pointlist = [(-1*self.curr_x,-1*self.curr_y)] # want to go to zero
        self.beginPointListExecution()
        print('Calibrating.....')
        self.closeWindow()
    def startRecord(self):
        self.record = True
        
    def stopRecord(self):
        self.record = False
        self.RUN_CONTINUOUS = False
        self.stopExecution()
        if self.record_run_toggle.isChecked():
            self.moveStage((0,0))
            if self.endTimer == None: # okay this works but its a hack not a solution.
                self.endTimer = QTimer(self)
                self.endTimer.setInterval(5000)
                self.endTimer.timeout.connect(self.handleEndCal)
            self.endTimer.start()
    def getRecording(self):
        return self.lbl,self.recorded_data, self.recorded_timestamps, self.unit, self.extra_info
    def clearRecord(self):
        self.recorded_data = []
        self.recorded_timestamps = []
    def plotRecorded(self,v,v_ts,ttl):
        pass
    def activate(self):
        if self.record_run_toggle.isChecked():
            # print('finished step 1: activate')
            self.RUN_CONTINUOUS = True
            self.handleShapeExecute()
        else:
            self.RUN_CONTINUOUS = False
    def handlePause(self):
        if self.pause_timer != None: 
            self.pause_timer.stop()
        self.paused = False
        # print('moving to next goal point')
        self.moveStage(self.curr_goal)
        
        
    def moveStage(self,coord):
        self.stage.go_to(coord[0],coord[1])
    
    #Go to points in a shape
    def go_to_points(self, numpoints, shape='square'):
        # amt is area for 2d shapes, length for 1d
        if shape == 'square':
            self.createSquarePointsList(numpoints)
        if shape == 'circle':
            self.createCircularPointsList(numpoints)
        if shape == 'line':
            self.createLinearPointsList(numpoints)
        # print('finished step 3: go to points')
        self.beginPointListExecution()
            
    def beginPointListExecution(self):
        if self.move_timer is None:
            # print('made move timer')
            #create the timer if not already there (i.e. executing the first point in the list
            self.move_timer = QTimer(self)
            self.move_timer.setInterval(50) 
            self.move_timer.timeout.connect(self.executePointsList)
        self.move_timer.start()
        # print('finished step 4: begin point list execution')
            
    #Go to points in a square
    def createSquarePointsList(self, numpoints,mode='long'):
        #Generates Points
        
        #ensure that points list is empty
        self.pointlist = []
        
        num_chunks = 4
        chunk_size = int(numpoints/num_chunks)
        # mid_pt_x = self.xmin + ((self.xmax - self.xmin) / 2)
        # mid_pt_y = self.ymin + ((self.ymax - self.ymin) / 2)
        
        
        if mode == 'random':
            # create random values for the x and y coordinates. 
            x_spaced = np.random.uniform(self.xmin,self.xmax,numpoints)
            y_spaced = np.random.uniform(self.ymin,self.ymax,numpoints)
           
            # x_spaced = self.createRandomVals(numpoints,min_val,length)
            # y_spaced = self.createRandomVals(numpoints,min_val,length)
            # x_spaced = self.createRandomVals(numpoints,6000,10000)
            # y_spaced = self.createRandomVals(numpoints,0,3000)
        elif mode == 'even dist':
            x_spaced = np.round(np.linspace(self.xmin,self.xmax,numpoints))
            y_spaced = np.round(np.linspace(self.ymin,self.ymax,numpoints))
        elif mode == 'long':
            tmp_pts_list = []
            for i in range(int(self.xmin),int(self.xmax),250):
                self.createLinearPointsList(numpoints,axis='y',const_val=i)
                for k in range(len(self.pointlist)):
                    tmp_pts_list.append(self.pointlist[k])
            # for h in range(0,12500,500):
            #     self.createLinearPointsList(numpoints,axis='x',const_val=h)
            #     for k in range(len(self.pointlist)):
            #         tmp_pts_list.append(self.pointlist[k])
            self.pointlist = tmp_pts_list    
        if mode != 'long':
            for i in range(len(y_spaced)):
                if i < len(x_spaced): # throw out invalid points
                    point = (x_spaced[i],y_spaced[i])
                    self.pointlist.append(point) # wont be optimal but will at least clump points in same quadrants - better would be sort by euclidean distance
        # print('populated ' + str(len(self.pointlist)) + ' points to points list')
              
            
    def createCircularPointsList(self, numpoints): 
        #Generates Points
        area = self.xmax
        sidelen = sqrt(area/np.pi)*2
        self.pointlist = []
        tmp_pointlist = []
        for i in range(numpoints):
            nopointyet = True
            while(nopointyet):
                randomX = round(np.random.uniform(0, sidelen))
                randomY = round(np.random.uniform(0, sidelen))
                if sqrt(randomX**2 + randomY**2) <= sidelen:
                    nopointyet = False
            tmp_pointlist.append((randomX, randomY))
        
        self.pointlist = tmp_pointlist
    def createLinearPointsList(self,numpoints,mode='random',axis='y',const_val=None):
        self.pointlist = []
        if const_val == None:
            const_val = self.xmax
        # tmp_pointlist = []
        if mode == 'random': 
            spaced = np.random.uniform(self.ymin,self.ymax,numpoints)
            # spaced = self.createRandomVals(numpoints,self.ymin,self.ymax)
        elif mode == 'even dist':
            spaced = np.round(np.linspace(self.ymin,self.ymax,numpoints))
        
        spaced.sort() # sort points in ascending order for faster execution
        mean = np.average(spaced)
        if self.curr_y > mean:
            #sort descending
            spaced = np.flip(spaced)
            
        for y in spaced:
            if axis == 'y':
                self.pointlist.append((const_val,y))  
            elif axis == 'x':
                self.pointlist.append((y,const_val))  
            
    def updateInputBoxes(self):
        if self.shape_select.currentText() == 'line':
            self.x_min_input.hide()
            self.x_min_lbl.hide()
            self.x_max_lbl.setText('Line Center (X):')
        else:
            self.x_min_input.show()
            self.x_min_lbl.show()
            self.x_max_lbl.setText('x max:')
            
    def createRandomVals(self,numpoints,min_val,max_val):
        spread = (max_val - min_val) / 5
        mid_pt = ((max_val-min_val)/2) + min_val
        pts = np.random.normal(mid_pt,spread,size=numpoints)
        valid_high_idx = pts<max_val
        valid_low_idx = pts>min_val
        new_pts = pts[valid_high_idx & valid_low_idx]
        return new_pts
    def stopExecution(self):
        if self.move_timer != None:
            self.move_timer.stop()
        if self.pause_timer != None:
            self.pause_timer.stop()
        self.paused = False
        self.curr_goal = (0,0)
        
        
    def executePointsList(self):
        if (not self.paused) and self.checkReached():
            if self.pointlist == []:#done executing commands
                if self.record and self.RUN_CONTINUOUS: # while recording sweep back and forth repeatedly
                    self.handleShapeExecute()
                else:
                    if self.is_calibrating:
                        # end calibration
                        self.stage.set_zero()
                        self.is_calibrating = False
                        print('Done Calibrating')
                    self.stopExecution()
            else:   
                # print('executing goal: '+str(self.curr_goal))
                self.curr_goal = self.pointlist.pop(0)
                if self.record:
                    self.paused = True
                    self.t_delay = True
                    # if self.transient_delay == None:
                    #     self.transient_delay = QTimer(self)
                    #     self.transient_delay.setInterval(300)
                    #     self.transient_delay.timeout.connect(self.handleTransientDelay)
                    if self.pause_timer == None:
                        self.pause_timer = QTimer(self)
                        self.pause_timer.setInterval(500)
                        self.pause_timer.timeout.connect(self.handlePause)
                    
                    # self.transient_delay.start()
                    self.pause_timer.start()
                else:
                    self.moveStage(self.curr_goal)
        if self.paused and self.record :#and (not self.t_delay):
            
            t = datetime.datetime.now()
            self.recorded_timestamps.append(datetimeToSeconds(t))
            self.recorded_data.append(str(self.curr_x)+' '+str(self.curr_y))
    # def handleTransientDelay(self):
    #     self.t_delay = False
    #     self.transient_delay.stop()
    def checkIdle(self):
        return self.stage.is_idle()
    def checkReached(self):
        curr_pose = self.stage.get_current_pos()
        self.curr_x = curr_pose[0]
        self.curr_y = curr_pose[1]
        
        threshold = 20
        high_x_thresh = self.curr_goal[0] + threshold
        low_x_thresh = self.curr_goal[0] - threshold
        high_y_thresh = self.curr_goal[1] + threshold
        low_y_thresh = self.curr_goal[1] - threshold
        reached_x_pose = (self.curr_x > low_x_thresh) and (self.curr_x < high_x_thresh)
        reached_y_pose = (self.curr_y > low_y_thresh) and (self.curr_y < high_y_thresh)
        if reached_y_pose and reached_x_pose:
            print('reached '+ str(self.curr_goal))
            return True
        else:
            return False
        
