# coding=utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QTableView
from PyQt4.QtCore import SIGNAL, QUrl
from StockMatchProperties import StockMatchProperties

class StockMatchTableView(QTableView):

    PROP_FINGER_SCROLLABLE = "FingerScrollable"

    def __init__(self):
        QTableView.__init__(self)

        self.prop = StockMatchProperties.instance()

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
#        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.setProperty(self.PROP_FINGER_SCROLLABLE, True)
        self.viewport().installEventFilter(self)

        self.connect(self, SIGNAL("doubleClicked(QModelIndex)"), self.doubleClicked)

    def doubleClicked(self, qModelIndex):

        tableModel = self.model()
        ticker = tableModel.getTicker(qModelIndex.row())
        googleUrl = self.prop.getGoogleUrl()
        url = "http://%s/finance?q=%s" % (googleUrl, ticker)
        print url
        self.openUrl(url)

    def openUrl(self, url):
        import os

        if os.name == 'posix':
            os.system('dbus-send --type=method_call --dest=com.nokia.osso_browser \
                       /com/nokia/osso_browser/request \
                       com.nokia.osso_browser.open_new_window \
                       string:%s' % (url))
        else:
            from PyQt4.Qt import QDesktopServices

            url = QUrl(url, QUrl.TolerantMode)
            QDesktopServices.openUrl(url)