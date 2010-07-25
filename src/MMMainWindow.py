from PyQt4 import  QtGui
from MMGoogleClientLoginDialog import MMGoogleClientLoginDialog
from PortfolioListView import *
from PyQt4.QtGui import QMainWindow, QWidget, QListView, QMenuBar, QComboBox, QGridLayout
from PyQt4.QtCore import qDebug
from MaeMoneyProperties import MaeMoneyProperties
from PositionWindow import PositionWindow
from Util import Util

class MMMainWindow(QMainWindow):

    PROP_FINGER_SCROLLABLE = "FingerScrollable"

    '''
    Redefined some of the attributes here such that Windows doesn't complain
    http://doc.qt.nokia.com/qt-maemo-4.6/qt.html#WidgetAttribute-enum
    '''
    
    WA_Maemo5StackedWindow = 127
    WA_Maemo5PortraitOrientation = 128
    WA_Maemo5LandscapeOrientation = 129
    WA_Maemo5AutoOrientation = 130
    WA_Maemo5ShowProgressIndicator = 131

    def __init__(self, controller):
        QMainWindow.__init__(self)
        self.prop = MaeMoneyProperties.instance()
        self.controller = controller
        self.loginDialog = MMGoogleClientLoginDialog(self)
        self.switchToLandscapeText = self.tr("Switch to Landscape")
        self.switchToPortraitText = self.tr("Switch to Portrait")
        self.setupUi()

    def setupUi(self):

        if self.prop.isPortraitMode():
            self.setAttributeAndCatch(self.WA_Maemo5PortraitOrientation, True)
            self.changeOrientationText = self.switchToLandscapeText
        else:
            self.setAttributeAndCatch(self.WA_Maemo5LandscapeOrientation, True)
            self.changeOrientationText = self.switchToPortraitText

        self.setWindowTitle(self.tr("MaeMoney"))
        self.setMinimumSize(QtCore.QSize(400, 400))
        self.gridLayout = QGridLayout()
        widget = QWidget(self)
        widget.setLayout(self.gridLayout)
        self.setCentralWidget(widget)

        self.btnLoadPortfolio = QtGui.QPushButton(self.tr("Sign in to Google Finance"))
        self.gridLayout.addWidget(self.btnLoadPortfolio, 0, 0, 1, 1)

        # List of portfolios
        self.portfolioListView = QComboBox()
        self.portfolioListView.setStyleSheet("QComboBox, QListView { font: 28px; } ")
        self.portfolioListView.setProperty(self.PROP_FINGER_SCROLLABLE, True)

        # Positions within the selected portfolio
        self.positionsListView = PortfolioListView(self)
        self.positionsListView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.positionsListView.setProperty(self.PROP_FINGER_SCROLLABLE, True)

        menuBar = QMenuBar()
        self.setMenuBar(menuBar)

        self.changeAppLocaleAction = QAction(self.tr("Change language"), self)
        menuBar.addAction(self.changeAppLocaleAction)

        self.changeUrlAction = QAction(self.tr("Change Google Finance URL"), self)
        menuBar.addAction(self.changeUrlAction)

        self.changeOrientationAction = QAction(self.changeOrientationText, self)
        menuBar.addAction(self.changeOrientationAction)

        self.changeUpdateIntervalAction = QAction(self.tr("Change update interval"), self)
        menuBar.addAction(self.changeUpdateIntervalAction)

    def changeOrientation(self):
        if self.prop.isPortraitMode():
            self.setAttributeAndCatch(self.WA_Maemo5LandscapeOrientation, True)
            self.prop.setPortraitMode(False)
            self.resize(800, 480)
            self.changeOrientationAction.setText(self.switchToPortraitText)
        else:
            self.setAttributeAndCatch(self.WA_Maemo5PortraitOrientation, True)
            self.prop.setPortraitMode(True)
            self.resize(480, 800)
            self.changeOrientationAction.setText(self.switchToLandscapeText)

        self.positionsListView.reset()


    def removeLoginButton(self):
        self.btnLoadPortfolio.setParent(None)
        self.gridLayout.removeWidget(self.btnLoadPortfolio)

    def setPortfolioListModel(self, model):
        self.gridLayout.addWidget(self.portfolioListView, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.positionsListView, 1, 1, 1, 1)
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


    def setBusyStatus(self, busy):
        try:
            self.setAttribute(self.WA_Maemo5ShowProgressIndicator, busy)
            from PyQt4.QtGui import QApplication
            QApplication.processEvents()
        except AttributeError:
            qDebug("Can't use WA_Maemo5ShowProgressIndicator")

    def setAttributeAndCatch(self, attribute, trueFalse):
        try:
            self.setAttribute(attribute, trueFalse)
        except AttributeError:
            qDebug("Can't set attribute %d" %(attribute))

    def showTransactionsForPosition(self, modelIndex):
        '''
        @param QModelIndex modelIndex
        '''

        exchange = self.positionsModel.getExchange(modelIndex)
        ticker = self.positionsModel.getTicker(modelIndex)
        position = self.positionsModel.getPositionData(modelIndex)

        self.setAttributeAndCatch(self.WA_Maemo5StackedWindow, True)
        transactionModel = self.controller.createTransactionModel(position)
        positionWin = PositionWindow(self, exchange, ticker, transactionModel)
        positionWin.show()

    def openWebpageForPosition(self, modelIndex):
        '''
        @param QModelIndex modelIndex
        '''

        exchange = self.positionsModel.getExchange(modelIndex)
        ticker = self.positionsModel.getTicker(modelIndex)
        exchangeTicker = "%s:%s" %(exchange, ticker)

        googleUrl = self.prop.getGoogleUrl()
        url = "http://%s/finance?q=%s" % (googleUrl, exchangeTicker)
        qDebug("Opening URL: %s" %(url))
        Util.openUrl(url)