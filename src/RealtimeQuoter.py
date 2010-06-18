# coding=utf-8

from Util import *
from PyQt4.QtCore import QObject, qDebug, SIGNAL
from MaeMoneyProperties import MaeMoneyProperties

class Updater(QObject):
    DEFAULT_UPDATE_INTERVAL_SECS = 8
    ABSOLUTE_MINIMUM_UPDATE_INTERVAL_SECS = 5

    def __init__(self, throttledQuoter):
        QObject.__init__(self)
        self._isRunning = False
        self.throttledQuoter = throttledQuoter
        self.setUpdateInterval(MaeMoneyProperties.instance().getUpdateInterval())
        self.exchangeTickerTuples = []
        self.connect(self.throttledQuoter, SIGNAL("quotesCached"), self.quotesUpdated)

    def setUpdateInterval(self, interval):
        if interval == 0:
            self.updateInterval = 0
        else:
            self.updateInterval = max(self.ABSOLUTE_MINIMUM_UPDATE_INTERVAL_SECS,
                                      interval)
        self.currentUpdateInterval = self.updateInterval

    def addTickers(self, tuple):
        self.exchangeTickerTuples.append(tuple)

    def start(self):
        self.tickersByExchange = self.groupTickersByExchange(self.exchangeTickerTuples)
        self.updateQuotes()
        if self.updateInterval > 0:
            self.timerId = self.startTimer(self.updateInterval * 1000)
            self._isRunning = True
        else:
            qDebug("Timer not started.")

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

    def timerEvent(self, event):
        self.updateQuotes()

    def terminate(self):
        if self._isRunning:
            self.killTimer(self.timerId)
            self._isRunning = False

    def updateQuotes(self):
        for exchange in self.tickersByExchange.keys():
            qDebug("Getting quotes for exchange: %s" %(exchange))
            symbols = self.tickersByExchange[exchange]
            self.throttledQuoter.updateCache(exchange, symbols)

        qDebug("[Updater] interval: %d" % (self.currentUpdateInterval))

    def isRunning(self):
        return self._isRunning

    def quotesUpdated(self):
        self.emit(SIGNAL("quotesUpdated"))
