#!/usr/bin/env python

import sys, os

from MMMainWindow import MMMainWindow
from MMController import MMController

from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QString, qDebug, QTranslator
from MaeMoneyProperties import MaeMoneyProperties

class MaeMoney:
    def __init__(self):
        self.controller = MMController()
        self.qMainWindow = MMMainWindow(self.controller)
        self.controller.setMainWindow(self.qMainWindow)
        self.controller.setLoginDialog(self.qMainWindow.loginDialog)
        self.qMainWindow.show()

qtApp = QApplication(sys.argv)
qtApp.setProperty("FingerScrollBars", False)
qtApp.setStyleSheet("\
                QHeaderView::section { \
                  background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, \
                                    stop: 0   #616161, stop: 0.5 #505050, \
                                    stop: 0.6 #333333, stop: 1   #656565); \
                  font-size: 18px; \
                  border: 1px solid #616161; \
                } \
                \
                QTableView { \
                  font-size: 18px;\
                  background-color: #616161; \
                  border: 1px solid #616161; \
                } \
                \
                QTableView::item { \
                  background-color: white; \
                  color: #333333; \
                  selection-color: #ffffff; \
                  border: 1px solid #616161; \
                  padding: 8px; \
                } \
                \
                QTableView::item:selected { \
                  color: #ffffff; \
                  background-color: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5,\
                                                    stop: 0   #007000, stop: 0.1 #00bc00, \
                                                    stop: 0.9 #00cf00, stop: 1   #008000); \
                } \
                ")

# Find out the directory of this file, which has the localization files
# (Could have used QCoreApplication.applicationFilePath but it only
# returns the path to the python executable on the N900)
absFilePath = os.path.abspath(__file__)
dir = os.path.dirname(absFilePath)

prop = MaeMoneyProperties.instance()
locale = prop.getAppLocale()
translator = QTranslator()
loaded = translator.load(QString("app-") + locale.name(), dir)
if not loaded:
    qDebug("Cannot load %s locale from %s" %(locale.name(), dir))
qtApp.installTranslator(translator)

app = MaeMoney()
sys.exit(qtApp.exec_())
