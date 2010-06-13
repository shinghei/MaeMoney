from PyQt4 import  QtGui
from MMGoogleClientLoginDialog import MMGoogleClientLoginDialog
from PortfolioListView import *
from PyQt4.QtGui import QMainWindow, QLabel, QWidget, QListView, QMenuBar, QComboBox
from PyQt4.QtCore import SIGNAL, qDebug, QObject, Qt

class MMMainWindow(QMainWindow):

    PROP_FINGER_SCROLLABLE = "FingerScrollable"

    def __init__(self, controller):
        QMainWindow.__init__(self)
        self.controller = controller
        self.loginDialog = MMGoogleClientLoginDialog(self)
        self.setupUi()

    def setupUi(self):
        self.setupUiPortrait()
        self.setWindowTitle(self.tr("MaeMoney"))

    def setupUiPortrait(self):

        self.isPortrait = True

        try:
            self.setAttribute(Qt.WA_Maemo5PortraitOrientation, True)
        except AttributeError:
            qDebug("Cannot set orientation to portrait")
        self.setMaximumSize(QtCore.QSize(480, 800))

        self.gridLayout = QtGui.QGridLayout()
        widget = QWidget(self)
        widget.setLayout(self.gridLayout)
        self.setCentralWidget(widget)

        self.btnLoadPortfolio = QtGui.QPushButton(self.tr("Sign in to Google Finance"))
        self.gridLayout.addWidget(self.btnLoadPortfolio, 0, 0, 1, 1)

        self.portfolioListView = QComboBox()
        self.gridLayout.addWidget(self.portfolioListView, 1, 0, 1, 1)

        self.positionsListView = QListView()
        self.positionsListView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.positionsListView.setBatchSize(10)
        self.gridLayout.addWidget(self.positionsListView, 2, 0, 1, 1)

        self.positionsListView.setProperty(self.PROP_FINGER_SCROLLABLE, True)
        self.portfolioListView.setProperty(self.PROP_FINGER_SCROLLABLE, True)

        self.changeAppLocaleAction = QAction(self.tr("Change language"), self)
        self.changeUrlAction = QAction(self.tr("Change Google Finance URL"), self)

        menuBar = QMenuBar()
        menuBar.addAction(self.changeAppLocaleAction)
        menuBar.addAction(self.changeUrlAction)
        self.setMenuBar(menuBar)

    def setupUiLandscape(self):

        self.isPortrait = True        

        self.setMaximumSize(QtCore.QSize(800, 480))

        self.gridLayout = QtGui.QGridLayout()
        widget = QWidget(self)
        widget.setLayout(self.gridLayout)
        self.setCentralWidget(widget)

        self.btnLoadPortfolio = QtGui.QPushButton(self.tr("Sign in to Google Finance"))
        self.gridLayout.addWidget(self.btnLoadPortfolio, 0, 0, 1, 2)

        self.portfolioListView = PortfolioListView(self)
        self.gridLayout.addWidget(self.portfolioListView, 1, 0, 1, 1)

        self.positionsListView = QListView()
        self.positionsListView.setMinimumWidth(600)
        self.positionsListView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.positionsListView.setBatchSize(10)
#        self.positionsListView.setLayoutMode(QListView.Batched)
#        self.setFlow(QListView.LeftToRight)
#        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerItem)
        self.gridLayout.addWidget(self.positionsListView, 1, 1, 1, 1)

        self.positionsListView.setProperty(self.PROP_FINGER_SCROLLABLE, True)
        self.portfolioListView.setProperty(self.PROP_FINGER_SCROLLABLE, True)

        self.changeAppLocaleAction = QAction(self.tr("Change language"), self)
        self.changeUrlAction = QAction(self.tr("Change Google Finance URL"), self)

        menuBar = QMenuBar()
        menuBar.addAction(self.changeAppLocaleAction)
        menuBar.addAction(self.changeUrlAction)
        self.setMenuBar(menuBar)

    def removeLoginButton(self):
        self.btnLoadPortfolio.setParent(None)
        self.gridLayout.removeWidget(self.btnLoadPortfolio)

    def setPortfolioListModel(self, model):
        self.portfolioListView.setModel(model)

    def setPositionsModel(self, model):
        oldModel = self.positionsListView.model()
        self.positionsModel = model
        self.positionsListView.setModel(model)

        if oldModel is not None:
            del oldModel

    def setupPositionsViewDelegate(self):

        from PositionsViewDelegate import PositionsViewDelegate

        self.positionsViewDelegate = PositionsViewDelegate()
        self.positionsListView.setItemDelegate(self.positionsViewDelegate)

    def setupSelectionModel(self):
        selectionModel = self.positionsListView.selectionModel()
        self.connect(selectionModel,
                     SIGNAL("selectionChanged(QItemSelection)"),
                     self.entrySelected)

    def entrySelected(self, selected):
         pass
#        self.selectedPositionIndex = selected
#        tickerSelected = self.positionsModel.getTicker(self.selectedPositionIndex)

    def setBusyStatus(self, busy):
        try:
            self.setAttribute(Qt.WA_Maemo5ShowProgressIndicator, busy)
            from PyQt4.QtGui import QApplication
            QApplication.processEvents()
        except AttributeError:
            qDebug("Can't use WA_Maemo5ShowProgressIndicator")
