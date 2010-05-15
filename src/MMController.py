from gdata.finance.service import FinanceService
from PortfolioTableModel import *
from PortfolioListModel import *
from RealtimeQuoter import *
from threading import *
from PyQt4.Qt import QProgressDialog, QThread

class MMController:

    def __init__(self):
        self.gDataClient = FinanceService()
        self.clientLoginToken = None
        self.quoter = ThrottledQuoter(RealtimeQuoter())
        self.updateThreads = {}

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

            portfolio = portfolios[pIndex]
            portfolioTitle = portfolio.title.text.decode("utf-8")

            progressDialog.setLabelText("Loading portfolio %s (%d of %d)"
                                        %(portfolioTitle, pIndex + 1, numPortfolios))

            portfolioId = portfolio.id.text
            if self.updateThreads.has_key(portfolioId):
                self.updateThreads[portfolioId].exit()
                print "Terminating thread %s" %(portfolioId)

            positions = self.gDataClient.GetPositionFeed(portfolio)
            tickers = [[0 for col in range(2)] for row in range(len(positions.entry))]
            i = 0
            for position in positions.entry:
                tickers[i][0] = position.symbol.exchange
                tickers[i][1] = position.symbol.symbol
                i = i + 1

            self.updateThreads[portfolioId] = UpdateThread(portfolioTitle.encode('utf-8'), self.quoter, tickers)
#            self.updateThreads[portfolioId].start()
            progressValue = progressValue + progressValueInc
            progressDialog.setValue(progressValue)

        return listModel

    def createPortfolioTableModel(self, portfolio):
        array = self.getPortfolioPositions(portfolio)
        tm = PortfolioTableModel(array, ["Name", "Price", "Gain", "Mkt Cap"], self.quoter)

        return tm
