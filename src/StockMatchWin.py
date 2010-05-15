# coding=utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL, QUrl
from PyQt4.QtGui import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, \
                     QLineEdit, QPushButton, QTableView,QGridLayout

import sys
import traceback

from StockMatchTableDelegate import StockMatchTableDelegate
from StockMatchTableModel import StockMatchTableModel
from StockMatchGoogleFinance import *

class SMMainWindow(QMainWindow):
    PROP_FINGER_SCROLLABLE = "FingerScrollable"
    

    def __init__(self):
        QMainWindow.__init__(self)
        widget = QWidget(self)
        self.setCentralWidget(widget)
        self.hbox = QHBoxLayout(widget)
        self.vbox = QVBoxLayout()
        self.hbox.addLayout(self.vbox)

        self.lineEdit = QLineEdit()
        # Qt.WA_InputMethodEnabled (14)
#        self.lineEdit.setAttribute(Qt.WA_InputMethodEnabled)
        self.lookupButton = QPushButton(u"查詢 Lookup")
        self.openUrlButton = QPushButton("Google Finance")
        self.openUrlButton.setEnabled(False)
#        self.hkCheckbox = QCheckBox(StockMatchTableModel.COUNTRY_HK)

        self.vbox.addWidget(self.lineEdit)
        self.vbox.addWidget(self.lookupButton)
        self.vbox.addWidget(self.openUrlButton)
        self.numPad = QGridLayout()
        gridHSpacing = 0
        self.numPad.setHorizontalSpacing(gridHSpacing)
        singleButtonWidth = 58
        button1 = self.createNumKey("1", singleButtonWidth)
        button2 = self.createNumKey("2", singleButtonWidth)
        button3 = self.createNumKey("3", singleButtonWidth)
        button4 = self.createNumKey("4", singleButtonWidth)
        button5 = self.createNumKey("5", singleButtonWidth)
        button6 = self.createNumKey("6", singleButtonWidth)
        button7 = self.createNumKey("7", singleButtonWidth)
        button8 = self.createNumKey("8", singleButtonWidth)
        button9 = self.createNumKey("9", singleButtonWidth)
        button0 = self.createNumKey("0", 2 * singleButtonWidth + gridHSpacing)
        buttonCE = self.createNumKey("CE", singleButtonWidth)
        self.numPad.addWidget(button7, 0, 0, 1, 1)
        self.numPad.addWidget(button8, 0, 1, 1, 1)
        self.numPad.addWidget(button9, 0, 2, 1, 1)
        self.numPad.addWidget(button4, 1, 0, 1, 1)
        self.numPad.addWidget(button5, 1, 1, 1, 1)
        self.numPad.addWidget(button6, 1, 2, 1, 1)
        self.numPad.addWidget(button1, 2, 0, 1, 1)
        self.numPad.addWidget(button2, 2, 1, 1, 1)
        self.numPad.addWidget(button3, 2, 2, 1, 1)
        self.numPad.addWidget(button0, 3, 0, 1, 2)
        self.numPad.addWidget(buttonCE, 3, 2, 1, 1)
        self.vbox.addLayout(self.numPad)
#        self.vbox.addWidget(self.hkCheckbox)
        self.vbox.addStretch()

        self.model = StockMatchTableModel()
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setMinimumWidth(580)
        self.table.setWordWrap(False)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.table.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.table.setProperty(self.PROP_FINGER_SCROLLABLE, True)

        self.delegate = StockMatchTableDelegate()
        self.table.setItemDelegate(self.delegate)

        self.stockMatcher = StockMatchGoogleFinance()
        self.hbox.addWidget(self.table)

        self.setWindowTitle(u"查股坊 Stock Matcher")

        self.connect(self.lineEdit, SIGNAL("returnPressed()"), self.lookupButton.click)
        self.connect(self.lookupButton, SIGNAL("pressed()"), self.processNewQuery)
        self.connect(self.table.selectionModel(),
                     SIGNAL("selectionChanged(QItemSelection, QItemSelection)"),
                     self.entrySelected)
        self.connect(self.openUrlButton, SIGNAL("pressed()"), self.openUrl)
        self.connect(button0, SIGNAL("pressed()"), lambda: self.pressedNum(0) )
        self.connect(button1, SIGNAL("pressed()"), lambda: self.pressedNum(1) )
        self.connect(button2, SIGNAL("pressed()"), lambda: self.pressedNum(2) )
        self.connect(button3, SIGNAL("pressed()"), lambda: self.pressedNum(3) )
        self.connect(button4, SIGNAL("pressed()"), lambda: self.pressedNum(4) )
        self.connect(button5, SIGNAL("pressed()"), lambda: self.pressedNum(5) )
        self.connect(button6, SIGNAL("pressed()"), lambda: self.pressedNum(6) )
        self.connect(button7, SIGNAL("pressed()"), lambda: self.pressedNum(7) )
        self.connect(button8, SIGNAL("pressed()"), lambda: self.pressedNum(8) )
        self.connect(button9, SIGNAL("pressed()"), lambda: self.pressedNum(9) )
        self.connect(buttonCE, SIGNAL("pressed()"), self.pressedCE)

    def pressedCE(self):
        self.lineEdit.clear()

    def pressedNum(self, num):
        old = self.lineEdit.text()
        numStr = str(num)
        self.lineEdit.setText(old + numStr)

    def createNumKey(self, numStr, width):
        btn = QPushButton(numStr)
#        btn.setMinimumWidth(width)
        btn.setMaximumWidth(width)
        return btn

    def processNewQuery(self):
        queryString = self.lineEdit.text()
        matches = self.stockMatcher.match(queryString)
        if matches is None:
            self.model.clear()
        else:
            self.model.reset(matches)
            self.table.resizeRowsToContents()
            self.table.resizeColumnsToContents()

        self.lineEdit.setFocus(True)
        self.openUrlButton.setEnabled(False)

    def entrySelected(self, selected):
        '''
        selected (type: QItemSelection) represents the selected row
        '''

        # Obtain a list of QModelIndex for the selected row
        selectedIndexes = selected.indexes()
        if len(selectedIndexes) > 0:
            # Pick the first cell (doesn't matter which column)
            # Assume SingleSelection mode
            anyCell = selectedIndexes[0]
            # Now print the ticker
            tickerSelected = self.model.getTicker(anyCell)
            if tickerSelected and tickerSelected is not None:
                self.gFinanceUrlForSelectedTicker = "http://www.google.com.hk/finance?q=%s" %(tickerSelected)
                self.openUrlButton.setText("Google Finance\n" + tickerSelected)
                self.openUrlButton.setEnabled(True)
            else:
                self.openUrlButton.setText("Google Finance")
                self.openUrlButton.setEnabled(False)
        else:
            self.openUrlButton.setText("Google Finance")
            self.openUrlButton.setEnabled(False)            

    def openUrl(self):
        import os
        if os.name == 'posix':
            os.system('dbus-send --type=method_call --dest=com.nokia.osso_browser \
                       /com/nokia/osso_browser/request \
                       com.nokia.osso_browser.open_new_window \
                       string:%s' %(self.gFinanceUrlForSelectedTicker))
        else:
            from PyQt4.Qt import QDesktopServices
            url = QUrl(self.gFinanceUrlForSelectedTicker, QUrl.TolerantMode)
            QDesktopServices.openUrl(url)

         
