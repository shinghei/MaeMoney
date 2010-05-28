# coding=utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL, QUrl, Qt, qDebug
from PyQt4.QtGui import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, \
                        QLineEdit, QPushButton, QTableView, \
                        QGridLayout, QMenuBar,QAction

from StockMatchTableDelegate import StockMatchTableDelegate
from StockMatchTableModel import StockMatchTableModel
from StockMatchGoogleFinance import StockMatchGoogleFinance
from StockMatchTableView import StockMatchTableView
from GoogleFinanceUrlSetupDialog import GoogleFinanceUrlSetupDialog

class SMMainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        widget = QWidget(self)
        self.setCentralWidget(widget)
        self.hbox = QHBoxLayout(widget)
        self.vbox = QVBoxLayout()
        self.hbox.addLayout(self.vbox)

        self.lineEdit = QLineEdit()
        self.lookupButton = QPushButton(u"查詢 Lookup")

        self.vbox.addWidget(self.lineEdit)
        self.vbox.addWidget(self.lookupButton)
        self.numPadLayout = QGridLayout()
        gridHSpacing = 0
        self.numPadLayout.setHorizontalSpacing(gridHSpacing)
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
        self.numPadLayout.addWidget(button7, 0, 0, 1, 1)
        self.numPadLayout.addWidget(button8, 0, 1, 1, 1)
        self.numPadLayout.addWidget(button9, 0, 2, 1, 1)
        self.numPadLayout.addWidget(button4, 1, 0, 1, 1)
        self.numPadLayout.addWidget(button5, 1, 1, 1, 1)
        self.numPadLayout.addWidget(button6, 1, 2, 1, 1)
        self.numPadLayout.addWidget(button1, 2, 0, 1, 1)
        self.numPadLayout.addWidget(button2, 2, 1, 1, 1)
        self.numPadLayout.addWidget(button3, 2, 2, 1, 1)
        self.numPadLayout.addWidget(button0, 3, 0, 1, 2)
        self.numPadLayout.addWidget(buttonCE, 3, 2, 1, 1)
        self.numPadLayout.setHorizontalSpacing(gridHSpacing)
        self.vbox.addLayout(self.numPadLayout)
        self.vbox.addStretch()

        self.table = StockMatchTableView()
        self.hbox.addWidget(self.table)
        self.model = StockMatchTableModel()
        self.delegate = StockMatchTableDelegate()

        self.table.setModel(self.model)
        self.table.setItemDelegate(self.delegate)

        self.stockMatcher = StockMatchGoogleFinance()

        self.hbox.setStretchFactor(self.vbox, 1)
        self.hbox.setStretchFactor(self.table, 10)

        self.setWindowTitle(u"查股坊 Stock Matcher")

        self.connect(self.lineEdit, SIGNAL("returnPressed()"), self.lookupButton.click)
        self.connect(self.lookupButton, SIGNAL("clicked()"), self.processNewQuery)
        self.connect(button0, SIGNAL("pressed()"), lambda: self.pressedNum(0))
        self.connect(button1, SIGNAL("pressed()"), lambda: self.pressedNum(1))
        self.connect(button2, SIGNAL("pressed()"), lambda: self.pressedNum(2))
        self.connect(button3, SIGNAL("pressed()"), lambda: self.pressedNum(3))
        self.connect(button4, SIGNAL("pressed()"), lambda: self.pressedNum(4))
        self.connect(button5, SIGNAL("pressed()"), lambda: self.pressedNum(5))
        self.connect(button6, SIGNAL("pressed()"), lambda: self.pressedNum(6))
        self.connect(button7, SIGNAL("pressed()"), lambda: self.pressedNum(7))
        self.connect(button8, SIGNAL("pressed()"), lambda: self.pressedNum(8))
        self.connect(button9, SIGNAL("pressed()"), lambda: self.pressedNum(9))
        self.connect(buttonCE, SIGNAL("pressed()"), self.pressedCE)

        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()

        changeUrlAction = QAction(u"更改Google財經網址 (Change Google Finance URL)", self)
        self.connect(changeUrlAction, SIGNAL("triggered()"), self.changeUrl)

        menuBar = QMenuBar()
        menuBar.addAction(changeUrlAction)
        self.setMenuBar(menuBar)

    def changeUrl(self):
        gfDialog = GoogleFinanceUrlSetupDialog(self)
        gfDialog.show()

    def pressedCE(self):
        self.lineEdit.clear()

    def pressedNum(self, num):
        old = self.lineEdit.text()
        numStr = str(num)
        self.lineEdit.setText(old + numStr)

    def createNumKey(self, numStr, width):
        btn = QPushButton(numStr)
        btn.setMinimumWidth(width)
        btn.setMaximumWidth(width)
        return btn

    def processNewQuery(self):
        queryString = self.lineEdit.text()
        qDebug("processNewQuery %s" % (queryString))
        self.setBusyStatus(True)

        matches = self.stockMatcher.match(queryString)
        if matches is None:
            self.model.clear()
        else:
            self.model.reset(matches)

        self.setBusyStatus(False)

        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()
        self.lineEdit.setFocus(True)

    def setBusyStatus(self, busy):
        try:
            self.setAttribute(Qt.WA_Maemo5ShowProgressIndicator, busy)
            from PyQt4.QtGui import QApplication
            QApplication.processEvents()
        except AttributeError:
            qDebug("Can't use WA_Maemo5ShowProgressIndicator")
