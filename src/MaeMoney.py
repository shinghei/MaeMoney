#!/usr/bin/env python

#Now we include our MainWindow.py generated from pyuic4.
from MMMainWindow import *
from MMController import *

class MaeMoney:
    def __init__(self):
        self.controller = MMController()
        self.qMainWindow = MMMainWindow(self.controller)
        self.qMainWindow.show()

qtApp = QtGui.QApplication(sys.argv)
qtApp.setProperty("FingerScrollBars", False)
app = MaeMoney()
sys.exit(qtApp.exec_())
