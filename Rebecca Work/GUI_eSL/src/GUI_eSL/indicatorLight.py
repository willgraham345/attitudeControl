# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 12:51:22 2021

@author: Becca
"""
from PyQt5.QtGui import QColor,QPainter
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QWidget

class IndicatorLight(QWidget):
    def __init__(self,parent = None):
        super().__init__()#parent)
        self.light_colors = {
                'off' : QColor('red'),
                'on'  : QColor('green')
                }
        self._current_color = self.light_colors['off']
        self.a = False

    def set_active(self,active):
        self.a = active
        if active:
            self._current_color = self.light_colors['on']
        else:
            self._current_color = self.light_colors['off']
        self.update()
    def get_active(self):
        return self.a
    def paintEvent(self, event):
        p = QPainter(self)
        p.setBrush(self._current_color)
        p.setPen(QtCore.Qt.black)
        p.drawEllipse(self.rect().center(), 5, 5)