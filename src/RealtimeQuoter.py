import urllib2, re, time, sys, traceback
from Util import *
from PyQt4.Qt import QThread, qWarning, QTimer, SIGNAL, SIGNAL, QObject

class Country:
    """
    Country-specific way to retrieve stocks quotes based on the corresponding "exchange"
    """

    NEWLINE_RE = re.compile('\n')

    # Matches JSON objects.
    # [ { ... } ]
    JSON_RE = re.compile('\[[\s]*\{.*\}[\s]*\]')

    def __init__(self, encoding, domain):
        self.encoding = encoding
        self.baseUrl = "http://%s/finance/info?client=ig&infotype=infoquoteall&q=" %(domain)

    def mergeExchangeTickers(self, exchange, tickers):
        exchangeTickers = [None] * len(tickers)
        for i in range(len(tickers)):
            exchangeTickers[i] = exchange + ":" + tickers[i]

        return ",".join(exchangeTickers)

    def loadsJsonString(self, jsonSearched):
        if sys.version.startswith("2.6") or sys.version.startswith("3"):
            import json
            decodedStocks = json.loads(jsonSearched, encoding=self.encoding)
        else:
            import simplejson
            decodedStocks = simplejson.loads(jsonSearched, encoding=self.encoding)
        return decodedStocks

    def getRealTimeQuotes(self, exchange, tickers):
        exchangeTickers = self.mergeExchangeTickers(exchange, tickers)
        try:
            connection = urllib2.urlopen(self.baseUrl + exchangeTickers)
            raw_data = connection.read()
            connection.close()
            stripped = self.NEWLINE_RE.sub('', raw_data)
            jsonSearched = self.JSON_RE.search(stripped)
            jsonSearched = Util.evalJson(jsonSearched.group(0))
            decodedStocks = self.loadsJsonString(jsonSearched)
        except urllib2.HTTPError:
            qWarning("Cannot open url for " + exchangeTickers)
            return None
        except ValueError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            qWarning("ValueError:")
            qWarning(jsonSearched)
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            return None

        return decodedStocks

class RealtimeQuoter:
    def __init__(self):
        self.cn = Country("gbk", "www.google.com.cn")
        self.hk = Country("big5hkscs", "www.google.com.hk")
        self.us = Country("utf-8", "www.google.com")

    def getRealtimeQuote(self, exchange, tickers):
        country = self.selectCountry(exchange)
        decodedQuotes = country.getRealTimeQuotes(exchange, tickers)
        return decodedQuotes

    def selectCountry(self, exchange):
        if exchange == "HKG":
            country = self.hk
        elif exchange == "SHA" or exchange == "SHE":
            country = self.cn
        else:
            country = self.us

        return country

class ThrottledQuoter:
    def __init__(self, rtQuoter):
        self.rtQuoter = rtQuoter
        self.cachedQuotes = {}

    def cachedData(self, exchange, ticker, colName):
        key = exchange + ":" + ticker
        if self.cachedQuotes.has_key(key):
            quote = self.cachedQuotes[key]
            return quote[colName]
        else:
            return None

    def updateCache(self, exchange, symbols):
        '''
        @return True if update was successful
        '''
        quotes = self.rtQuoter.getRealtimeQuote(exchange, symbols)
        if quotes is None:
            return False

        n = len(symbols)
        for i in range(n):
            self.storeQuote(exchange, symbols[i], quotes[i])

        return True

    def storeQuote(self, exchange, ticker, quote):
        if quote is not None:
            key = exchange + ":" + ticker
            self.cachedQuotes[key] = quote

        # ---------- Accessors ---------------

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

class UpdateThread1(QThread):
    DEFAULT_UPDATE_INTERVAL_SECS = 15
    ABSOLUTE_MINIMUM_UPDATE_INTERVAL_SECS = 5

    def __init__(self, threadName, throttledQuoter, exchangeTickerTuples,
                 updateInterval=DEFAULT_UPDATE_INTERVAL_SECS, *args):
        self.throttledQuoter = throttledQuoter
        self.tickersByExchange = self.groupTickersByExchange(exchangeTickerTuples)
        self.stopped = False
        self.updateInterval = max(self.ABSOLUTE_MINIMUM_UPDATE_INTERVAL_SECS,
                                  updateInterval)
        self.currentUpdateInterval = self.updateInterval

        apply(QThread.__init__, (self, ) + args)
        self.name = threadName
        print "Thread %s started" % (self.name)
        QThread.startTimer()

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

    def run(self):

        self.success = True
        while self.success:
            self.updateQuotes()
            time.sleep(self.currentUpdateInterval)

    def updateQuotes(self):
        print "Time's up"
        self.success = True
        for exchange in self.tickersByExchange.keys():
            symbols = self.tickersByExchange[exchange]
            status = self.throttledQuoter.updateCache(exchange, symbols)
            self.success = self.success & status

        if not self.success:
            self.currentUpdateInterval = self.currentUpdateInterval * 2
        else:
            self.currentUpdateInterval = max(self.currentUpdateInterval / 2, self.updateInterval)

        print "[%s] Update interval: %d" %(self.name, self.currentUpdateInterval)


class UpdateThread(QObject):
    DEFAULT_UPDATE_INTERVAL_SECS = 15
    ABSOLUTE_MINIMUM_UPDATE_INTERVAL_SECS = 5

    def __init__(self, threadName, throttledQuoter, exchangeTickerTuples,
                 updateInterval=DEFAULT_UPDATE_INTERVAL_SECS):
        QObject.__init__(self)
        self.throttledQuoter = throttledQuoter
        self.tickersByExchange = self.groupTickersByExchange(exchangeTickerTuples)
        self.stopped = False
        self.updateInterval = max(self.ABSOLUTE_MINIMUM_UPDATE_INTERVAL_SECS,
                                  updateInterval)
        self.currentUpdateInterval = self.updateInterval
        self.name = threadName

        self.updateQuotes()

        self.timerId = QObject.startTimer(self, self.updateInterval * 1000)

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

    def run(self):

        self.success = True
        while self.success:
            self.updateQuotes()
            time.sleep(self.currentUpdateInterval)

    def timerEvent(self, event):
        self.updateQuotes()

    def terminate(self):
        QObject.killTimer(self.timerId)

    def updateQuotes(self):
        print "Time's up"
        self.success = True
        for exchange in self.tickersByExchange.keys():
            symbols = self.tickersByExchange[exchange]
            status = self.throttledQuoter.updateCache(exchange, symbols)
            self.success = self.success & status

        if not self.success:
            self.currentUpdateInterval = self.currentUpdateInterval * 2
        else:
            self.currentUpdateInterval = max(self.currentUpdateInterval / 2, self.updateInterval)

        print "[%s] Update interval: %d" %(self.name, self.currentUpdateInterval)


