#!/usr/bin/env python

import sys
import os
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QString, QTranslator
from StockMatchProperties import StockMatchProperties
from PyQt4.QtCore import qDebug

if __name__ == '__main__':
    qtApp = QApplication(sys.argv)
    qtApp.setProperty("FingerScrollBars", False)

    # Find out the directory of this file, which has the localization files
    # (Could have used QCoreApplication.applicationFilePath but it only
    # returns the path to the python executable on the N900)
    absFilePath = os.path.abspath(__file__)
    dir = os.path.dirname(absFilePath)

    prop = StockMatchProperties.instance()
    locale = prop.getAppLocale()
    translator = QTranslator()
    loaded = translator.load(QString("app-") + locale.name(), dir)
    if not loaded:
        qDebug("Cannot load %s locale from %s" %(locale.name(), dir))
    qtApp.installTranslator(translator)

    from StockMatchWin import SMMainWindow
    win = SMMainWindow()
    win.show()
    sys.exit(qtApp.exec_())
