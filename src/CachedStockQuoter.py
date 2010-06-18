import sys
from PyQt4.QtCore import QCoreApplication, QObject, QUrl, SIGNAL, qDebug
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest
from MaeMoneyProperties import MaeMoneyProperties
from Util import Util
import re

class CachedStockQuoter(QObject):

    # Matches JSON objects.
    # [ { ... } ]
    JSON_RE = re.compile('\[[\s]*\{.*\}[\s]*\]')

    def __init__(self):
        QObject.__init__(self)
        self.cachedQuotes = {}
        self.prop = MaeMoneyProperties.instance()
        self.baseUrl = "http://%s/finance/info?client=ig&infotype=infoquoteall&q=%s"
        self.networkMgr = QNetworkAccessManager()
        self.connect(self.networkMgr, SIGNAL("finished(QNetworkReply*)"), self.replyFinished)

    def updateCache(self, exchange, symbols):
        concatTickers = self.mergeExchangeTickers(exchange, symbols)
        gUrl = self.prop.getGoogleUrl()
        qDebug("[CachedStockQuoter] Google URL: %s" %(gUrl))
        url = self.baseUrl %(gUrl, concatTickers)
        self.initiateGetQuote(url)

    def mergeExchangeTickers(self, exchange, tickers):
        exchangeTickers = [None] * len(tickers)
        for i in range(len(tickers)):
            exchangeTickers[i] = exchange + ":" + tickers[i]

        return ",".join(exchangeTickers)

    def initiateGetQuote(self, url):
        qUrl = QUrl(url)
        request = QNetworkRequest(qUrl)
        self.networkMgr.get(request)

    def replyFinished(self, reply):
        '''
        @param reply QNetworkReply
        '''
        payload = reply.readAll().data()
        reply.deleteLater()

        self.processPayload(payload)

    def processPayload(self, payload):
        stripped = Util.removeNewLine(payload)

        jsonRegexResult = self.JSON_RE.search(stripped)
        jsonRegexMatched = jsonRegexResult.group(0)

        jsonRegexMatched = Util.evalJson(jsonRegexMatched)
        jsonObjects = Util.loadsJsonString(jsonRegexMatched, "utf-8")
        for jsonObj in jsonObjects:
            exchange = jsonObj['e']
            symbol = jsonObj['t']
            self.storeQuote(exchange, symbol, jsonObj)

        self.emit(SIGNAL("quotesCached"))

    def storeQuote(self, exchange, symbol, quote):
        key = exchange + ":" + symbol
        if self.cachedQuotes.has_key(key):
            oldQuote = self.cachedQuotes[key]
            oldQuote.clear()
        self.cachedQuotes[key] = quote

    def groupTickersByExchange(self, exchangeTickerTuples):
        grouped = {}
        for ticker in exchangeTickerTuples:
            exchange = ticker[0]
            symbol = ticker[1]
            if not grouped.has_key(exchange):
                grouped[exchange] = []
            tickerList = grouped[exchange]
            tickerList.append(symbol)

        return grouped

    # ---------- Accessors ---------------

    def cachedData(self, exchange, ticker, colName):
        key = exchange + ":" + ticker
        if self.cachedQuotes.has_key(key):
            quote = self.cachedQuotes[key]
            return quote[colName]
        else:
            return ""

    def getChangePercentage(self, exchange, ticker):
        return self.cachedData(exchange, ticker, "cp")

    def getChange(self, exchange, ticker):
        return self.cachedData(exchange, ticker, "c")

    def getFullName(self, exchange, ticker):
        return self.cachedData(exchange, ticker, "name")

    def getMarketCap(self, exchange, ticker):
        return self.cachedData(exchange, ticker, "mc")

    def getPrice(self, exchange, ticker):
        return self.cachedData(exchange, ticker, "l_cur")

    def getColor(self, exchange, ticker):
        return self.cachedData(exchange, ticker, "ccol")

    def getPeRatio(self, exchange, ticker):
        return self.cachedData(exchange, ticker, "pe")

    def getDelay(self, exchange, ticker):
        return self.cachedData(exchange, ticker, "delay")

    def getVolume(self, exchange, ticker):
        return self.cachedData(exchange, ticker, "vo")

    def getAverageVolume(self, exchange, ticker):
        return self.cachedData(exchange, ticker, "avvo")

if __name__ == '__main__':
    qtApp = QCoreApplication(sys.argv)
    app = CachedStockQuoter()
    app.updateCache("NYSE", ["MCD", "GE"])
    app.updateCache("HKG", ["0811", "0927", "0888", "3918", "0050", "1991"])
    sys.exit(qtApp.exec_())