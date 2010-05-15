#!/usr/bin/env python

import sys
from PyQt4.QtGui import QApplication
from StockMatchWin import SMMainWindow

if __name__ == '__main__':
    qtApp = QApplication(sys.argv)
    qtApp.setProperty("FingerScrollBars", False)
    win = SMMainWindow()
    win.show()
    sys.exit(qtApp.exec_())
