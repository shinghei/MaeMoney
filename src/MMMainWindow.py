from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from MMGoogleClientLoginDialog import MMGoogleClientLoginDialog
from MMController import *
from PortfolioListModel import *
from PortfolioTableDelegate import *
from RightClickEventHandler import *
from PortfolioListView import *
from PyQt4.Qt import QLabel

class MMMainWindow(QMainWindow):

    PROP_FINGER_SCROLLABLE = "FingerScrollable"

    def __init__(self, controller):
        QMainWindow.__init__(self)
        self.controller = controller
        self.loginDialog = MMGoogleClientLoginDialog(self, self.controller)
        self.setupUi()

    def setupUi(self):

        self.setMaximumSize(QtCore.QSize(800, 480))

        self.gridLayout = QtGui.QGridLayout()
        widget = QWidget(self)
        widget.setLayout(self.gridLayout)
        self.setCentralWidget(widget)

        self.btnLoadPortfolio = QtGui.QPushButton()
        self.gridLayout.addWidget(self.btnLoadPortfolio, 0, 0, 1, 1)

        self.portfolioListView = PortfolioListView(self)
        self.gridLayout.addWidget(self.portfolioListView, 1, 0, 1, 1)

        self.statusLabel = QLabel("<-- Click here to login to Google Finance")
        self.gridLayout.addWidget(self.statusLabel, 0, 1, 1, 1)
        self.portfolioEntriesTableView = QtGui.QTableView()
        self.portfolioEntriesTableView.setWordWrap(True)
        self.portfolioEntriesTableView.setMinimumWidth(600)
        self.portfolioEntriesTableView.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.portfolioEntriesTableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.portfolioEntriesTableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gridLayout.addWidget(self.portfolioEntriesTableView, 1, 1, 1, 1)

        self.portfolioEntriesTableView.setProperty(self.PROP_FINGER_SCROLLABLE, True)
        self.portfolioListView.setProperty(self.PROP_FINGER_SCROLLABLE, True)

        self.retranslateUi()
        self.connect(self.btnLoadPortfolio,
                     SIGNAL("clicked()"),
                     self.loadPortfolio)
        self.connect(self.portfolioListView,
                     SIGNAL("clicked(QModelIndex)"),
                     self.portfolioSelected)
        self.connect(self.loginDialog,
                     SIGNAL("accepted()"),
                     self.loginAccepted)
       
    def retranslateUi(self):
        self.setWindowTitle(QApplication.translate("MMMainWindow", "MaeMoney", None, QApplication.UnicodeUTF8))
        self.btnLoadPortfolio.setText(QApplication.translate("MMMainWindow", "Load Portfolio", None, QApplication.UnicodeUTF8))

    def loginAccepted(self):
        self.loadPortfolio()

    def loadPortfolio(self):
        if self.controller.isLoggedIn():
            # @todo WA_Maemo5ShowProgressIndicator

            progress = QProgressDialog("Bootstrapping data", QString(), 0, 100, self)
            progress.setWindowModality(Qt.WindowModal)
            self.portfolioListModel = self.controller.createPortfolioListModel(progress)
            self.portfolioListView.setModel(self.portfolioListModel)
            progress.setValue(100)
        else:
            self.loginDialog.show()

    def portfolioSelected(self, qModelIndex):
        progress = QProgressDialog("Loading positions from portfolio", QString(), 0, 0, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.forceShow()

        p = self.portfolioListModel.getPortfolio(qModelIndex)
        progress.setLabelText("Retreiving data from Google Finance")

        self.portfolioTableModel = self.controller.createPortfolioTableModel(p)

        self.portfolioEntriesTableView.setModel(self.portfolioTableModel)

        self.portfolioEntriesTableView.resizeColumnsToContents()

        progress.close()
                
        selectionModel = self.portfolioEntriesTableView.selectionModel()
        self.connect(selectionModel,
                     QtCore.SIGNAL("selectionChanged(QItemSelection, QItemSelection)"),
                     self.entrySelected)

        self.portfolioTableDelegate = PortfolioTableDelegate()
        self.portfolioEntriesTableView.setItemDelegate(self.portfolioTableDelegate)
        self.portfolioEntriesTableView.resizeRowsToContents()
        self.portfolioEntriesTableView.resizeColumnsToContents()
        
    def entrySelected(self, selected):
        '''
        selected (type: QItemSelection) represents the selected row
        '''

        # Obtain a list of QModelIndex for the selected row
        selectedIndexes = selected.indexes()
        # Pick the first cell (doesn't matter which column)
        anyCell = selectedIndexes[0]
        # Now print the ticker
        tickerSelected = self.portfolioTableModel.getTicker(anyCell)
        self.statusLabel.setText(tickerSelected)

        