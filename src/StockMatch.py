#!/usr/bin/env python

import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QString, QTranslator
from StockMatchProperties import StockMatchProperties

if __name__ == '__main__':
    qtApp = QApplication(sys.argv)
    qtApp.setProperty("FingerScrollBars", False)

    prop = StockMatchProperties.instance()
    locale = prop.getAppLocale()
    translator = QTranslator()
    translator.load(QString("app-") + locale.name())
    qtApp.installTranslator(translator)

    from StockMatchWin import SMMainWindow
    win = SMMainWindow()
    win.show()
    sys.exit(qtApp.exec_())
