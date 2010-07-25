# coding=utf-8

from gdata.finance.service import FinanceService
from PositionsModel import PositionsModel
from PortfolioListModel import *
from RealtimeQuoter import *
from PyQt4.QtCore import qDebug, SIGNAL
from GoogleFinanceUrlSetupDialog import GoogleFinanceUrlSetupDialog
from PyQt4.QtGui import QProgressDialog, QApplication
from AppLocaleSetupDialog import AppLocaleSetupDialog
from CachedStockQuoter import CachedStockQuoter
from UpdateIntervalDialog import UpdateIntervalDialog
from TransactionsModel import TransactionsModel

class MMController(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.gDataClient = FinanceService()
        self.clientLoginToken = None
        self.quoter = CachedStockQuoter()
        self.updater = None
        self.positionsModel = None

    def setLoginDialog(self, loginDialog):
        self.loginDialog = loginDialog
        self.connect(self.loginDialog,
                     SIGNAL("credentialsEntered(QString, QString)"),
                     self.processCredentials)
        self.connect(self.loginDialog,
                     SIGNAL("accepted()"),
                     self.loginAccepted)

    def setMainWindow(self, mainWindow):
        self.mainWindow = mainWindow

        self.connect(self.mainWindow.btnLoadPortfolio,
                     SIGNAL("clicked()"),
                     self.loadPortfolio)

        self.connect(self.mainWindow.positionsListView,
                     SIGNAL("doubleClicked(QModelIndex)"),
                     self.mainWindow.showTransactionsForPosition)

        self.connect(self.mainWindow.portfolioListView,
                     SIGNAL("activated(int)"),
                     self.portfolioSelectedComboBox)

        self.connect(self.mainWindow.changeAppLocaleAction,
                     SIGNAL("triggered()"),
                     self.changeLocale)

        self.connect(self.mainWindow.changeUrlAction,
                     SIGNAL("triggered()"),
                     self.changeUrl)

        self.connect(self.mainWindow.changeOrientationAction,
                     SIGNAL("triggered()"),
                     self.changeOrientation)

        self.connect(self.mainWindow.changeUpdateIntervalAction,
                     SIGNAL("triggered()"),
                     self.changeUpdateInterval)

    def changeUpdateInterval(self):
        updateIntervalDialog = UpdateIntervalDialog(self.mainWindow, self.updater)
        updateIntervalDialog.show()

    def changeOrientation(self):
        self.mainWindow.changeOrientation()

    def changeLocale(self):
        localeDialog = AppLocaleSetupDialog(self.mainWindow)
        localeDialog.show()

    def changeUrl(self):
        gfDialog = GoogleFinanceUrlSetupDialog(self.mainWindow)
        gfDialog.show()

    def portfolioSelectedComboBox(self, index):
        self.mainWindow.setBusyStatus(True)
        p = self.portfolioListModel.getPortfolioByRow(index)
        self.positionsModel = self.createPositionsModel(p)

        self.mainWindow.setPositionsModel(self.positionsModel)
        self.mainWindow.setupPositionsViewDelegate()
        self.mainWindow.setBusyStatus(False)

    def portfolioSelected(self, qModelIndex):
        self.mainWindow.setBusyStatus(True)

        p = self.portfolioListModel.getPortfolio(qModelIndex)
        self.positionsModel = self.createPositionsModel(p)

        self.mainWindow.setPositionsModel(self.positionsModel)
        self.mainWindow.setupSelectionModel()
        self.mainWindow.setupPositionsViewDelegate()

        self.mainWindow.setBusyStatus(False)

    def loadPortfolio(self):
        if self.isLoggedIn():
            self.portfolioListModel = self.createPortfolioListModel()
            self.mainWindow.setPortfolioListModel(self.portfolioListModel)
        else:
            self.loginDialog.show()

    def loginAccepted(self):
        self.mainWindow.removeLoginButton()
        self.loadPortfolio()
        if self.portfolioListModel:
            if self.portfolioListModel.rowCount() > 0:
                self.portfolioSelectedComboBox(0)
            else:
                # @todo Inform user to create portfolio on Google Finance website.
                qWarning("Inform user to create portfolio on Google Finance website.")

    def login(self, userName, password):
        self.userName = userName
        self.gDataClient.ClientLogin(userName, password)
        self.clientLoginToken = self.gDataClient.GetClientLoginToken()

    def isLoggedIn(self):
        if self.clientLoginToken is not None:
            return True
        else:
            return False

    def getPortfolios(self):
        portfolios = self.gDataClient.GetPortfolioFeed()
        return portfolios.entry

    def getPortfolioPositions(self, portfolio):

        positions = self.gDataClient.GetPositionFeed(portfolio)
        portfolioPositions = [0 for row in range(len(positions.entry))]
        i = 0
        for position in positions.entry:
            portfolioPositions[i] = {}
            portfolioPositions[i]['exchange'] = position.symbol.exchange
            portfolioPositions[i]['ticker'] = position.symbol.symbol
            portfolioPositions[i]['name'] = position.symbol.full_name
            portfolioPositions[i]['change'] = "0.0"
            portfolioPositions[i]['changePct'] = "0.0%"
            # Save the position object such that transactions can be fetched later on
            portfolioPositions[i]['position'] = position

            i = i + 1

        return portfolioPositions

    '''
    @param positionData - PostionData
    @return TransactionsModel
    '''
    def createTransactionModel(self, positionData):
        transactionFeed = self.gDataClient.GetTransactionFeed(positionData)
        transactions = transactionFeed.entry
        transactionModel = TransactionsModel(transactions)
        return transactionModel

    def createPortfolioListModel(self):

        portfolios = self.getPortfolios()
        listModel = PortfolioListModel(portfolios)
        numPortfolios = len(portfolios)

        progress = QProgressDialog(self.tr("Loading portfolios from Google"), QString(), 0, numPortfolios, self.mainWindow)
        progress.setWindowTitle(self.tr("Loading portfolios from Google"))

        if self.updater:
            self.updater.terminate()
            self.disconnect(self.updater, SIGNAL("quotesUpdated"), self.processQuotesUpdated)

        self.updater = Updater(self.quoter)       
        QObject.connect(self.updater, SIGNAL("quotesUpdated"), self.processQuotesUpdated)

        for pIndex in range(numPortfolios):

            portfolio = portfolios[pIndex]
            positions = self.gDataClient.GetPositionFeed(portfolio)
            for position in positions.entry:
                tickerTuple = position.symbol.exchange, position.symbol.symbol
                self.updater.addTickers(tickerTuple)

            portfolioName = portfolio.title.text.decode("utf-8")
            labelText = QString("'%s' (%d / %d)" %(portfolioName, pIndex + 1, numPortfolios))
            progress.setLabelText(labelText)
            progress.setValue(pIndex + 1)
            QApplication.processEvents()

        self.updater.start()

        return listModel

    def createPositionsModel(self, portfolio):
        array = self.getPortfolioPositions(portfolio)
        pm = PositionsModel(array, self.quoter)

        return pm

    def processQuotesUpdated(self):
        qDebug("[MMController] processQuotesUpdated")
        if self.positionsModel:
            self.positionsModel.emitModelReset()

    def processCredentials(self, userName, password):

        from gdata.service import BadAuthentication, CaptchaRequired

        try:
            self.login(userName, password)
            self.loginDialog.acceptCredentials(userName, password)
        except BadAuthentication:
            self.loginDialog.rejectCredentials("BadAuthentication: Wrong username or password.")
        except CaptchaRequired:
            self.loginDialog.rejectCredentials("CaptchaRequired: Wrong username or password.")
