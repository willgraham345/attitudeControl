# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 17:13:46 2021

@author: Wintermute
"""
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QEventLoop
import datetime
class Worker(QThread):
    data = pyqtSignal(str)
    def __init__(self, cont=True , parent=None):
        QThread.__init__(self, parent)
        self.running = False
        self.check_info=None
        self.cont = cont

    def run(self):
        self.running = True
        while self.running:
            self.getData()
    def stop(self):
        self.running = False
        self.wait()
    def getData(self):
        info = self.check_info()
        self.data.emit(info)
