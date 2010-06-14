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
