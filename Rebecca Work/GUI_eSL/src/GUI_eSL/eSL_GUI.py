# -*- coding: utf-8 -*-
"""
Created on Tues Jun 21 15:28:06 2022

@author: Becca
"""

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QMainWindow, QApplication, QLineEdit, QMessageBox, QSpacerItem, QComboBox, QCheckBox
from PyQt5.QtGui import QFont, QDoubleValidator, QIntValidator
import sys
import os
from StageWidget import XYStageWidget
from PyQt5.QtCore import QSize, QTimer, Qt
from serial.tools import list_ports
from device_definitions import Device
from indicatorLight import IndicatorLight
from PyQt5.QtCore import QSize, QTimer, Qt, pyqtSignal
from tkinter import filedialog
from GUI_supporting_functions import Element, ForceSensorWidget
import tkinter as tk
from ScopeWidget import OscilloscopeWidget
import csv
import time
import matplotlib.pyplot as plt
import datetime
import pyvisa
class SensorsWindow(QMainWindow):
    '''
    This is the main GUI window, it handles all jobs that are not device specific
    '''
    def __init__(self):
        QMainWindow.__init__(self)
        self.init_gui()
        self.connected_devices = []
        self.all_widgets = []
        
        self.supply = None
        self.anemometer = None
        self.timer = None
        self.cnt = 0
        
    def init_gui(self):
        '''
        Window Settings
        '''
        self.setMinimumSize(QSize(800, 420))    
        self.setWindowTitle("Experiment Tools") 
        
        self.window = QWidget()
        self.layout = QGridLayout()
        self.setCentralWidget(self.window)
        self.window.setLayout(self.layout)
        lbl_font = QFont('Arial',11)
        #spacer that helps keep GUI items where I tell them to go in the layout
        spacer_item = QSpacerItem(1, 1) 
        '''
        Force Sensor 
        '''
        self.force = None
        self.force_indicator = IndicatorLight()
        self.force_widget = QLabel("Force Data: ",self)
        self.force_widget.setFont(lbl_font)

        '''
        Save Filename Input
        '''
        self.save_file_lbl = QLabel('filename:')
        self.save_file_lbl.setFont(lbl_font)
        self.save_file_box = QLineEdit()  
        '''
        Run Experiment Button
        '''
        self.experiment_button = QPushButton(self)
        self.experiment_button.setText("Run Experiment")
        self.experiment_button.clicked.connect(self.runExperiment)
        '''
        Detect Connected USB Devices Button
        '''
        self.detect_button = QPushButton(self)
        self.detect_button.setText("Detect") # detect connected USB devices
        self.detect_button.clicked.connect(self.getDevices)
        self.detect_USB_devices = Element(this_widget=self.detect_button)
        '''
        Oscilloscope
        '''
        self.oscilloscope = None
        self.num_channels = 4
        self.ch1_lbl = QLabel('Ch 1')
        self.ch1_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.ch2_lbl = QLabel('Ch 2')
        self.ch2_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.ch3_lbl = QLabel('Ch 3')
        self.ch3_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.ch4_lbl = QLabel('Ch 4')
        self.ch4_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        device_options = ['Voltage Monitor','Current Monitor','Anemometer','Ground','None']
        
        self.ch1 = QComboBox()#QLineEdit('Shunt Resistor')
        self.ch1.addItems(device_options)
        self.ch1.setCurrentIndex(0)
        self.ch2 = QComboBox()#QLineEdit('Anemometer')
        self.ch2.addItems(device_options)
        self.ch2.setCurrentIndex(1)
        self.ch3 = QComboBox() #QLineEdit('None')
        self.ch3.addItems(device_options)
        self.ch3.setCurrentIndex(2)
        self.ch4 = QComboBox()#QLineEdit('None')
        self.ch4.addItems(device_options)
        self.ch4.setCurrentIndex(4)
        self.scope_indicator = IndicatorLight()
        self.scope_lbl = QLabel('Oscilloscope Settings')
        self.scope_lbl.setFont(lbl_font)
        
        self.scope_onoff = QPushButton(self)
        self.scope_onoff.setText('...')
        
        self.range_lbl = QLabel('Set Volt Scale: (V/div)')
        self.range_unit_lbl = QLabel('V/div')
        self.ch1_range_in = QLineEdit('1.0')
        self.ch1_range_in.setValidator(QDoubleValidator())
        self.ch2_range_in = QLineEdit('1.0')
        self.ch2_range_in.setValidator(QDoubleValidator())
        self.ch3_range_in = QLineEdit('1.0')
        self.ch3_range_in.setValidator(QDoubleValidator())
        self.ch4_range_in = QLineEdit('1.0')
        self.ch4_range_in.setValidator(QDoubleValidator())
                
        self.range_set_btn = QPushButton()
        self.range_set_btn.setText('Update')
        
        self.plt_ttl_lbl = QLabel('Plot Title: ')
        self.ch1_plt_ttl = QLineEdit(device_options[0])
        self.ch2_plt_ttl = QLineEdit(device_options[1])
        self.ch3_plt_ttl = QLineEdit(device_options[2])
        self.ch4_plt_ttl = QLineEdit(device_options[2])
        
        self.plt_toggle_lbl = QLabel('Show Plot')
        self.ch1_plt_toggle = QCheckBox()
        # self.ch1_plt_toggle.setChecked(True)
        self.ch1_plt_toggle.stateChanged.connect(self.updatePlotOptions)
        self.ch2_plt_toggle = QCheckBox()
        # self.ch2_plt_toggle.setChecked(True)
        self.ch2_plt_toggle.stateChanged.connect(self.updatePlotOptions)
        self.ch3_plt_toggle = QCheckBox()
        # self.ch3_plt_toggle.setChecked(False)
        self.ch3_plt_toggle.stateChanged.connect(self.updatePlotOptions)
        self.ch4_plt_toggle = QCheckBox()
        # self.ch4_plt_toggle.setChecked(False)
        self.ch4_plt_toggle.stateChanged.connect(self.updatePlotOptions)
        
        plt_mode_options = ['Vs. Supply Voltage','Vs. Time']
        self.plt_mode_lbl = QLabel('Plot Type: ')
        self.ch1_plt_mode = QComboBox()
        self.ch1_plt_mode.addItems(plt_mode_options)
        self.ch2_plt_mode = QComboBox()
        self.ch2_plt_mode.addItems(plt_mode_options)
        self.ch3_plt_mode = QComboBox()
        self.ch3_plt_mode.addItems(plt_mode_options)
        self.ch4_plt_mode = QComboBox()
        self.ch4_plt_mode.addItems(plt_mode_options)
        
        
        scope_offset_lbl = QLabel('Offset (V):')
        scope_offset_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.scope_offset_input = QLineEdit('-3.5')
        self.scope_offset_input.setValidator(QDoubleValidator())
        self.scope_offset_btn = QPushButton()
        self.scope_offset_btn.setText('Update')
        self.scope_offset_chan_sel = QComboBox()
        self.scope_offset_chan_sel.addItems(['all','ch1','ch2','ch3','ch4'])
        
        self.plt_checkboxes = [self.ch1_plt_toggle,self.ch2_plt_toggle,self.ch3_plt_toggle,self.ch4_plt_toggle]
        self.plt_modes = [self.ch1_plt_mode,self.ch2_plt_mode,self.ch3_plt_mode,self.ch4_plt_mode]
        self.plt_titles = [self.ch1_plt_ttl,self.ch2_plt_ttl,self.ch3_plt_ttl,self.ch4_plt_ttl]
        self.updatePlotOptions()
        full_scope_widget = [self.ch1,self.ch2,self.ch3,self.ch4,
                             self.scope_onoff,self.ch1_range_in,
                             self.ch2_range_in,self.ch3_range_in,
                             self.ch4_range_in,self.range_set_btn,
                             self.scope_offset_input,self.scope_offset_chan_sel,self.scope_offset_btn]     
        '''
        XY Stage
        '''
        self.xy_stage = None
        self.xy_stage_indicator = IndicatorLight()
        self.stage_lbl = QLabel('XY Stage')
        self.stage_lbl.setFont(lbl_font)
        self.stage_calibrate_btn = QPushButton(self)
        self.stage_calibrate_btn.setText('Calibrate')
        stage_shape_lbl = QLabel('Collector Shape')
        self.stage_shape_sel = QComboBox()
        self.stage_shape_sel.addItems(['square','line','circle'])
        stage_samp_lbl = QLabel('Number of Samples')
        self.stage_num_samples = QLineEdit('8')
        self.stage_num_samples.setValidator(QIntValidator())
        self.x_min_lbl = QLabel('x min:')
        self.x_min_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.x_min_input = QLineEdit('0')
        self.x_min_input.setValidator(QIntValidator())
        self.x_max_lbl = QLabel('x max:')
        self.x_max_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.x_max_input = QLineEdit('10000')
        self.x_max_input.setValidator(QIntValidator())
        self.y_min_lbl = QLabel('y min:')
        self.y_min_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.y_min_input = QLineEdit('0')
        self.y_min_input.setValidator(QIntValidator())
        self.y_max_lbl = QLabel('y max:')
        self.y_max_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.y_max_input = QLineEdit('10000')
        self.y_max_input.setValidator(QIntValidator())
        
        # self.stage_shape_sel.currentIndexChanged.connect(self.updateStageText)
        stage_goto_lbl = QLabel('Go To:')
        stage_goto_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        stage_goto_lbl_x = QLabel('X')
        stage_goto_lbl_x.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        stage_goto_lbl_y = QLabel('Y')
        stage_goto_lbl_y.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        stage_goto_unit_lbl = QLabel('Micrometer')
        self.stage_goto_x = QLineEdit('0')
        self.stage_goto_x.setValidator(QDoubleValidator())
        self.stage_goto_y = QLineEdit('0')
        self.stage_goto_y.setValidator(QIntValidator())
        self.stage_goto_go = QPushButton(self)
        self.stage_goto_go.setText('Go')
        self.stage_shape_execute_btn = QPushButton()
        self.stage_shape_execute_btn.setText('Execute Shape')
        self.stage_go_home_btn = QPushButton()
        self.stage_go_home_btn.setText('Go Home')
        self.stage_activate_lbl = QLabel('Use XY Stage Shape')
        self.stage_activate_toggle = QCheckBox()
        self.stage_curr_pose_txt = QLabel('Curr Pose: (0, 0)')
        full_stage_widget = [self.stage_calibrate_btn, 
                       self.stage_num_samples,
                       self.stage_shape_sel, 
                       # self.stage_size_input,self.stage_size_min,
                       self.stage_shape_execute_btn,
                       self.stage_goto_x,self.stage_goto_y,self.stage_goto_go,self.stage_go_home_btn,
                       self.stage_activate_toggle,
                       self.stage_curr_pose_txt,
                       self.x_min_input,self.x_max_input,self.y_min_input,self.y_max_input,self.x_min_lbl,self.x_max_lbl
                       ]
        '''
        Reference Dictionaries 
        '''
        #These dictionaries associate serial numbers with devices/widgets- this is what enables automatic device detection and activation
        self.possible_devices = {
                            'ME30YTTDA' : Device('ME30YTTDA' , 'force_sensor'),
                            '0001'      : Device('0001', 'power_supply'),
                            'ad2'       : Device('ad2', 'discovery'),
                            'AB0JHGH2A' : Device('AB0JHGH2A','anemometer'),
                            'silly'     : Device('silly','oscilloscope'),
                            '95036303335351B061F0' : Device('95036303335351B061F0','xy_stage')
                            }
        self.possible_widgets = {
                            'force_sensor' : ForceSensorWidget(this_widget=self.force_widget,indicator=self.force_indicator,lbl='Force'),
                            'oscilloscope' : OscilloscopeWidget(this_widget=full_scope_widget,indicator=self.scope_indicator,lbl='Oscilloscope'),
                            'xy_stage'     : XYStageWidget(this_widget=full_stage_widget,indicator=self.xy_stage_indicator,lbl='XY Stage')
                            }
        '''
        Layout Arrangement
        '''
        # Layout : widget, row, col, row_span, col_span
        self.layout.addWidget(self.detect_button,0,0,1,1)
        self.layout.addWidget(self.save_file_lbl, 0, 2, 1, 2)
        self.layout.addWidget(self.save_file_box,0,4,1,5)
        # self.layout.addItem(spacer_item,0,,1,10)
        self.layout.addWidget(self.experiment_button,0,10,1,1)
        
        
        self.layout.addWidget(self.force_indicator,2,0,1,1)
        self.layout.addWidget(self.force_widget,2,1,1,3)
        self.layout.addItem(spacer_item,2,5,1,2)        
        
        self.layout.addItem(spacer_item,3,5,1,2)  
        self.layout.addWidget(self.supply_indicator,3,7,1,1)
        self.layout.addWidget(sweep_lbl,3,8,1,1)
        self.layout.addWidget(self.sweep_set,3,9,1,1)
        self.layout.addWidget(self.sweep_go,3,10,1,1)
        
        self.layout.addWidget(self.scope_indicator,4,0,1,1)
        self.layout.addWidget(self.scope_lbl, 4, 1, 1, 1)
        self.layout.addItem(spacer_item,4,2,1,1)
        self.layout.addWidget(self.scope_onoff,4,3,1,1) 
        self.layout.addItem(spacer_item,4,4,1,6)
        
        # self.layout.setAlignment(Qt.AlignRight)
        self.layout.addWidget(scope_offset_lbl,5,1,1,1)
        self.layout.addWidget(self.scope_offset_input,5,2,1,1)  
        self.layout.addWidget(self.ch1_lbl,5,3,1,1)
        self.layout.addWidget(self.ch1,5,4,1,1)
        self.layout.addWidget(self.ch2_lbl,5,5,1,1)
        self.layout.addWidget(self.ch2,5,6,1,1)
        self.layout.addWidget(self.ch3_lbl,5,7,1,1)
        self.layout.addWidget(self.ch3,5,8,1,1)
        self.layout.addWidget(self.ch4_lbl,5,9,1,1)
        self.layout.addWidget(self.ch4,5,10,1,1)
        
        # self.layout.addItem(spacer_item,6,1,1,2)
        
        self.layout.addWidget(self.scope_offset_chan_sel,6,1,1,1)
        self.layout.addWidget(self.scope_offset_btn,6,2,1,1)
                            
        self.layout.addWidget(self.range_lbl,6,3,1,1)
        self.layout.addWidget(self.ch1_range_in, 6, 4, 1, 1)
        self.layout.addWidget(self.ch2_range_in, 6, 6, 1, 1)
        self.layout.addWidget(self.ch3_range_in, 6, 8, 1, 1)
        self.layout.addWidget(self.ch4_range_in, 6, 10, 1, 1)
        self.layout.addWidget(self.range_set_btn, 6, 11, 1, 1)
        
        self.layout.addItem(spacer_item,7,1,1,1)
        self.layout.addWidget(self.plt_toggle_lbl, 7, 3, 1, 1)
        self.layout.addWidget(self.ch1_plt_toggle, 7, 4, 1, 1)
        self.layout.addWidget(self.ch2_plt_toggle, 7, 6, 1, 1)
        self.layout.addWidget(self.ch3_plt_toggle, 7, 8, 1, 1)
        self.layout.addWidget(self.ch4_plt_toggle, 7, 10, 1, 1)
        
        # self.layout.addWidget(shunt_lbl,10,1,1,1)
        # self.layout.addWidget(self.shunt_input,10,2,1,1)
        # self.layout.addWidget(shunt_unit,10,3,1,1)
        # self.layout.addItem(spacer_item,10,4,1,7)  
        
        # self.layout.addItem(spacer_item,11,0,1,11) #ruuuude, wont display
        
        self.layout.addWidget(self.xy_stage_indicator,12,0,1,1)
        self.layout.addWidget(self.stage_lbl,12,1,1,1)
        self.layout.addWidget(self.stage_calibrate_btn,12,2,1,1)
        self.layout.addWidget(self.stage_activate_lbl,12,3,1,1)
        self.layout.addWidget(self.stage_activate_toggle, 12, 4, 1, 1)
        self.layout.addItem(spacer_item,12,5,6)
        
        self.layout.addItem(spacer_item,13,0,1,1)
        self.layout.addWidget(stage_shape_lbl,13,1,1,1)
        self.layout.addWidget(self.stage_shape_sel,13,2,1,1)
        # self.layout.addWidget(self.stage_size_lbl,13,3,1,1)
        # self.layout.addWidget(self.stage_size_min,13,4,1,1)
        # self.layout.addWidget(self.stage_size_input,13,5,1,1)
        # self.layout.addWidget(self.stage_size_unit,13,6,1,1)
        self.layout.addWidget(self.x_min_lbl,13,3,1,1)
        self.layout.addWidget(self.x_min_input,13,4,1,1)
        self.layout.addWidget(self.x_max_lbl,13,5,1,1)
        self.layout.addWidget(self.x_max_input,13,6,1,1)
        
        self.layout.addWidget(stage_samp_lbl,13,7,1,1)
        self.layout.addWidget(self.stage_num_samples,13,8,1,1)
        self.layout.addWidget(self.stage_shape_execute_btn,13,9,1,1)
        self.layout.addItem(spacer_item,13,10,1,1)
        
        
        self.layout.addItem(spacer_item,14,0,1,4)
        self.layout.addWidget(self.y_min_lbl,14,3,1,1)
        self.layout.addWidget(self.y_min_input,14,4,1,1)
        self.layout.addWidget(self.y_max_lbl,14,5,1,1)
        self.layout.addWidget(self.y_max_input,14,6,1,1)
        self.layout.addItem(spacer_item,14,7,1,3)
        
        self.layout.addItem(spacer_item,15,1,1,1)
        self.layout.addWidget(stage_goto_lbl,15,2,1,1)
        self.layout.addWidget(stage_goto_lbl_x, 15, 3, 1, 1)
        self.layout.addWidget(self.stage_goto_x, 15, 4, 1, 1)
        self.layout.addWidget(stage_goto_lbl_y, 15, 5, 1, 1)
        self.layout.addWidget(self.stage_goto_y, 15, 6, 1, 1)
        self.layout.addWidget(stage_goto_unit_lbl,15,7,1,1)
        self.layout.addWidget(self.stage_goto_go,15,8,1,1)
        self.layout.addItem(spacer_item,15,9,2)
        
        self.layout.addItem(spacer_item,16,0,1,2)
        self.layout.addWidget(self.stage_go_home_btn,16,3,1,1)
        self.layout.addWidget(self.stage_curr_pose_txt,16,4,1,1)
        self.layout.addItem(spacer_item,16,4,7)
        
    def updatePlotOptions(self):
        '''
        These are checkboxes that enable plots to pop up after an experiment 
        finishes. 
        ***The plotting functionality has not been maintained so it may or may 
        not work well currently, better is to use one of the plotting scripts 
        to read the saved data and plot that way.***
        '''
        for i in range(len(self.plt_checkboxes)):
            this_box = self.plt_checkboxes[i]
            this_ttl = self.plt_titles[i]
            this_mode = self.plt_modes[i]
            if this_box.isChecked():
                this_ttl.show()
                this_mode.show()
            else:
                this_ttl.hide()
                this_mode.hide()
    def closeEvent(self,event):
        '''
        This shuts off communication with all connected devices and stops all
        currently running timers so that the program closes cleanly and doesnt
        have already open serial communications which prevents the program from
        being able to run again without restarting the console
        '''
        if self.timer != None:
            self.timer.stop()
        for tw in self.all_widgets:
            tw.close()
 
    def getDevices(self):
        '''
        detect what devices are connected and activate the UI for each detected
        device.
        '''
        self.detectDevices(True) # check for connected device, set verbose
        self.displayAllDeviceUIs()

    def displayAllDeviceUIs(self):
        '''
        Connects each found device to its appropriate GUI widget 
        '''
        for device in self.connected_devices:
            already_found = False #dont try to re-initialize a device that is already set up 
            identifier = device.device_id
            ui = self.possible_widgets[identifier]
            # each ui refers to an object which contains both all the information
            # and functions which operate each device and their interface on the 
            # GUI as a whole.
            for w in self.all_widgets:
                if w.lbl == ui.lbl:
                    already_found = True
            if not already_found:
                ui.tied_device = device
                # If a specific device has been identified, associate it with a variable 
                # so that the GUI can access it if there are device specific actions that 
                # the top-level interface needs to access.
                if ui.lbl == 'Oscilloscope':
                    self.oscilloscope = ui
                elif ui.lbl == 'Power Supply':
                    self.supply = ui
                elif ui.lbl == 'Anemometer': #note: this is the old anemometer not the one that connects to the oscilloscope. That one is just an oscilloscope signal
                    self.anemometer = ui
                elif ui.lbl == 'Force':
                    self.force = ui
                elif ui.lbl == 'XY Stage':
                    self.xy_stage = ui
                self.all_widgets.append(ui)
                ui.start()

    def detectDevices(self,verbose=False):
        """
        description: determines what devices are connected to the USB ports
            it will update the COM ports that each found device is connected
            to and return the list of found devices
            connected_devices (list) -
                list of widgets which control the devices that are connected to the computer
        input:  verbose (boolean) -
                    if true, will print messages
        """
        # Get a list of every device connected to a usb port on the computer
        available_ports = list_ports.comports()
        self.connected_devices = []
        if verbose:
            print("found ",len(available_ports), " ports")
        self.checkForAD2(verbose) # The analog discovery has more complicated connection than the rest so check for that separately. 
        self.checkForOscilloscope(verbose)
        for port in available_ports:
            serial_num = port.serial_number 
            port_id = port.name
            device = self.possible_devices[serial_num] #check the dictionary for a valid device. Use the serial number to identify the different devices as they are most likely to be unique
            device.serial_port = port_id
            if not self.checkConnected(device):
                self.connected_devices.append(device)
                if verbose:
                    print(device.device_id, " found on port ", device.serial_port)
    def checkConnected(self,device):
        '''
        check if a device has already been registered as being connected
        i.e. only store one instance of each device even if the "detect" 
        button has been pressed multiple times.
        '''
        for d in self.connected_devices:
            if d.device_id == device.device_id:
                return True 
        return False
    def checkForOscilloscope(self,verbose):
        '''
        The oscilloscope uses pyvisa to communicate. This means it needs 
        slightly special treatment to find. 
        *** currently this seems to have a bug and the program wont run without 
        the oscilloscope turned on. Not sure how to fix this as of yet.***
        '''
        rm = visa.ResourceManager()
        scope_id = 'USB0::0x1AB1::0x04CE::DS1ZA232705605::INSTR'
        try:
            if scope_id in rm.list_resources():
                serial_num = 'silly'
                device = self.possible_devices[serial_num]
                self.connected_devices.append(device)
                if verbose:
                    print('Found Oscilloscope')
        except:
            pass # if scope isnt available (fix bug????)
    def runExperiment(self):
        '''
        Triggered when the user clicks the "run experiment" buton. 
        Prompts the user to choose a directory to save to,
        Data is saved to directory with the specified title 
        each instruments data is saved to a separate file within the directory
        '''
        if self.supply is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Power Supply Not Connected')
            msg.setWindowTitle("Error")
            msg.exec_()
        else:
            self.full_path = ''
            savefile = self.checkFilename()
            if savefile != None:
                # Prompt for directory to save to, then create sub directory
                root = tk.Tk()
                root.withdraw()
                chosen_dir = filedialog.askdirectory()
                self.path = chosen_dir + '/' + savefile
                # if file already exists, add increment to name to guarantee unique names
                if os.path.exists(self.path):
                    
                    i=0
                    test_path = self.path
                    while os.path.exists(test_path):
                        i=i+1
                        test_path = self.path + ' (' + str(i) + ')'
                    self.path = test_path
                os.mkdir(self.path) 
                # Run Experiment
                # Allow setups to settle before recording then tell devices to begin recording
                # wait for 2 seconds to record pre-experiment baseline 
                # then activate the power supply and signal generator
                time.sleep(0.5) # Allow setups to settle before beginning recording
                # make sure all recordings start fresh
                for k in self.all_widgets:
                    k.clearRecord()
                t = datetime.datetime.now()
                print('recording started at ' + str(t.time()))
                for w in self.all_widgets:
                    w.startRecord() 
                # The timing for the recording is controlled by the power supply 
                # (running its voltage sweep, when the sweep finishes the recording ends)
                # as such, the power supply controls the oscilloscope. 
                # *** This will likely need to change a bit with the new High Voltage supply
                # as that cuts out the "normal voltage" power supply from the system ***
                self.supply.attachScope(self.oscilloscope)
                time.sleep(1)
                self.wait = QTimer()
                self.wait.setInterval(2000) #continue after 2 second delay
                self.wait.timeout.connect(self.activatePower)
                self.wait.start()
            #wait until done
    def activatePower(self):
        '''
        This function controls the start/stop of a running experiment. 
        it is only called by the timer which controls the experiment setup 
        so the first step here is to shut off that timer or else the function
        will get called multiple times (the timer will continue timing out every 
        2 seconds until it is shut off. we only want it to activate once per experiment)
        '''
        self.wait.stop()
        
        # perform pre-experiment last moment setups for the xy stage and power supply.
        # the power supply activation is what actually begins the experiment running.
        if self.xy_stage is not None:
            self.xy_stage.activate()
        self.supply.activate()
        # Wait until experiment is finished
        self.timer = QTimer(self)
        self.timer.setInterval(1) #check for the end of the experiment every 1 mS
        self.timer.timeout.connect(self.checkEnd)
        self.timer.start()
    
        self.experiment_button.setText('Stop Experiment') # allows for user to abort the experiment
        self.experiment_button.clicked.disconnect(self.runExperiment)
        self.experiment_button.clicked.connect(self.handleSweepFinish)
        
    def checkEnd(self):
        '''
        The power supply will raise a flag signifying that it has finished its sweep
        this checks to see if that flag has been raised each time the timer times out (every 1mS)
        '''
        if self.supply.checkDone():
            self.timer.stop()
            self.handleSweepFinish()            
    def handleSweepFinish(self):
        '''
        Once the power supply has finished its sweep, stop recording, 
        save the data and display plots if necessary. 
        '''
        for w in self.all_widgets:
            w.stopRecord()
        shunt = float(self.shunt_input.text()) # shunt resistor value
        # This manages the optional plots that can show up after an experiment is finished.
        if self.supply != None:
            l,ps_v,ps_ts,u,e = self.supply.getRecording()
            fig_cnt = 1
            if self.oscilloscope != None: 
                self.oscilloscope.setShuntR(shunt, self.shunt_unit_txt)
                for i in range(self.num_channels):
                    this_box = self.plt_checkboxes[i]
                    chan = i+1
                    if this_box.isChecked():
                        plt.figure(fig_cnt)
                        this_ttl = self.plt_titles[i]
                        this_mode = self.plt_modes[i]
                        mode_sel = 'cv'
                        if this_mode.currentText() == 'Vs. Time':
                            mode_sel = 'time'
                        splot = self.oscilloscope.plotRecorded(ps_v,ps_ts,this_ttl.text(),channel_select=chan,mode=mode_sel)
                        splot.show()
                        fig_cnt +=1 
            if self.anemometer != None:
                plt.figure(fig_cnt)
                fig_cnt +=1
                aneplot = self.anemometer.plotRecorded(ps_v,ps_ts,self.ivel_plt_ttl.text())
                aneplot.show()
            if self.force != None:
                plt.figure(fig_cnt)
                fig_cnt +=1
                forceplot = self.force.plotRecorded(ps_v,ps_ts,self.vf_plt_ttl.text())
                forceplot.show()
        
        self.Save()#save data to files
        if self.experiment_button.text() == 'Stop Experiment': # reset the experiment buttons
            self.experiment_button.setText('Run Experiment')
            self.experiment_button.clicked.disconnect(self.handleSweepFinish)    
            self.experiment_button.clicked.connect(self.runExperiment)
        print('Finished Experiment')
    def checkFilename(self):
        '''
        check to ensure the user has entered a valid name to save the data to 
        when they run an experiment. Throw error if no name has been entered
        '''
        name = self.save_file_box.text()
        if name == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Must enter a valid filename to save to')
            msg.setWindowTitle("Error")
            msg.exec_()
            return None
        else:
            return name
    def Save(self):  
        '''
        Save recorded data
        '''
        time.sleep(1)
        print('Saving Data....')
        # Go through each device that has been connected, retrieve the data recorded 
        # from each and write it to a file
        for w in self.all_widgets:
            lbl = ''
            data = []
            timestamps = []
            unit = ''
            extra_info = ''
            # the oscilloscope file has data from each channel so the saved file is in a 
            # slightly different format than the rest of the save files 
            
            if w.lbl == 'Oscilloscope':
                channels = [self.ch1.currentText(),self.ch2.currentText(),self.ch3.currentText(),self.ch4.currentText()]
                for i in range(len(channels)):
                    # 'None' indicates nothing is connected to that channel
                    if channels[i] != 'None':
                        # give channel number and instrument name (input text)
                        l,d,ts,u,ei = w.getRecording(i+1,channels[i])
                        self.writeToFile(l,d,ts,u,ei)
            else:
                lbl,data,timestamps,unit,extra_info = w.getRecording()
                self.writeToFile(lbl, data, timestamps, unit, extra_info)

        print('Done Saving')
    def writeToFile(self,lbl,data,timestamps,unit,extra_info):   
        '''
        This function is what physically writes the text into each saved file. 
        '''         
        filename = lbl + '.csv'
        self.full_path = self.path + '/' + filename
        with open(self.full_path, mode='w',newline='') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
            #make header, first 3 lines of the file are always header info
            writer.writerow([lbl])
            writer.writerow([unit])
            writer.writerow([extra_info])
            # write each datapoint with its associated timestamp
            for i in range(len(data)):
                d = data[i]
                ts = timestamps[i]
                writer.writerow([d, ts])  
        
if __name__ == "__main__":
    '''
    This starts the GUI as an application and allows the user to close the GUI 
    using the red x button
    '''
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True) 
    mainWin = SensorsWindow()
    mainWin.show()
    sys.exit( app.exec() )