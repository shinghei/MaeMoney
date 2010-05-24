from gdata.finance.service import FinanceService
from PortfolioTableModel import *
from PortfolioListModel import *
from RealtimeQuoter import *
from threading import *
from PyQt4.QtCore import qDebug, QThread, QEventLoop, SIGNAL
from PyQt4.QtGui import QProgressDialog, QApplication

class MMController(QObject):

    def __init__(self):
        self.gDataClient = FinanceService()
        self.clientLoginToken = None
        self.quoter = ThrottledQuoter(RealtimeQuoter())
        self.updaters = {}

    def setLoginDialog(self, loginDialog):
        self.loginDialog = loginDialog
        self.connect(self.loginDialog,
                     SIGNAL("credentialsEntered(string, string)"),
                     self.processCredentials)
        self.connect(self.loginDialog,
                     SIGNAL("accepted()"),
                     self.loginAccepted)


    def setMainWindow(self, mainWindow):
        self.mainWindow = mainWindow

        self.connect(self.mainWindow.btnLoadPortfolio,
                     SIGNAL("clicked()"),
                     self.loadPortfolio)
        self.connect(self.mainWindow.portfolioListView,
                     SIGNAL("clicked(QModelIndex)"),
                     self.portfolioSelected)


    def portfolioSelected(self, qModelIndex):
        progress = QProgressDialog("Loading positions from portfolio", QString(), 0, 0, self.mainWindow)
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimum(0)
        progress.setMaximum(0)
        progress.show()

        p = self.portfolioListModel.getPortfolio(qModelIndex)
        progress.setLabelText("Retreiving data from Google Finance")
        self.portfolioTableModel = self.createPortfolioTableModel(p)
        self.mainWindow.setPortfolioTableModel(self.portfolioTableModel)

        progress.close()

        self.mainWindow.setupSelectionModel()
        self.mainWindow.setupPortfolioTableDelegate()
        self.mainWindow.autoFitPortfolioTable()

    def loadPortfolio(self):
        if self.isLoggedIn():
            progress = QProgressDialog("Bootstrapping data", QString(), 0, 100, self.mainWindow)
            progress.setWindowModality(Qt.WindowModal)
            self.portfolioListModel = self.createPortfolioListModel(progress)
            self.mainWindow.setPortfolioListModel(self.portfolioListModel)
            progress.setValue(100)
        else:
            self.loginDialog.show()

    def loginAccepted(self):
        self.loadPortfolio()

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

            i = i + 1

        return portfolioPositions

    def createPortfolioListModel(self, progressDialog):
        '''
        @param progressDialog QProgressDialog
        '''
        
        portfolios = self.getPortfolios()
        listModel = PortfolioListModel(portfolios)
        numPortfolios = len(portfolios)
        progressValue = 0
        progressValueInc = progressDialog.maximum() / (numPortfolios + 1)

        for pIndex in range(numPortfolios):

            QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
            
            portfolio = portfolios[pIndex]
            portfolioTitle = portfolio.title.text.decode("utf-8")

            progressDialog.setLabelText("Loading portfolio %s (%d of %d)"
                                        %(portfolioTitle, pIndex + 1, numPortfolios))

            portfolioId = portfolio.id.text
            if self.updaters.has_key(portfolioId):
                self.updaters[portfolioId].terminate()
                qDebug("Terminating thread %s" %(portfolioId))

            positions = self.gDataClient.GetPositionFeed(portfolio)
            tickers = [[0 for col in range(2)] for row in range(len(positions.entry))]
            i = 0
            for position in positions.entry:
                tickers[i][0] = position.symbol.exchange
                tickers[i][1] = position.symbol.symbol
                i = i + 1

            self.updaters[portfolioId] = Updater(portfolioTitle.encode('utf-8'), self.quoter, tickers)

            QObject.connect(self.updaters[portfolioId], SIGNAL("quotesUpdated"), self.processQuotesUpdated)

            progressValue = progressValue + progressValueInc
            progressDialog.setValue(progressValue)

        return listModel

    def createPortfolioTableModel(self, portfolio):
        array = self.getPortfolioPositions(portfolio)
        tm = PortfolioTableModel(array, ["Name", "Price", "Gain", "Mkt Cap"], self.quoter)

        return tm

    def processQuotesUpdated(self):
        print "updated"

    def processCredentials(self, userName, password):

        from gdata.service import BadAuthentication, CaptchaRequired
        import base64
        
        try:
            self.login(userName, password)
            self.loginDialog.acceptCredentials(userName, password)
        except BadAuthentication:
            self.loginDialog.rejectCredentials("BadAuthentication: Wrong username or password.")
        except CaptchaRequired:
            self.loginDialog.rejectCredentials("CaptchaRequired: Wrong username or password.")
