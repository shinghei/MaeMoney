#!/usr/bin/env python

from MMMainWindow import MMMainWindow
from MMController import MMController

from PyQt4.QtGui import QApplication
import sys

class MaeMoney:
    def __init__(self):
        self.controller = MMController()
        self.qMainWindow = MMMainWindow(self.controller)
        self.controller.setMainWindow(self.qMainWindow)
        self.controller.setLoginDialog(self.qMainWindow.loginDialog)
        self.qMainWindow.show()

qtApp = QApplication(sys.argv)
qtApp.setProperty("FingerScrollBars", False)
app = MaeMoney()
sys.exit(qtApp.exec_())
