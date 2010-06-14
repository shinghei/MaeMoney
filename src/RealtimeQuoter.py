# coding=utf-8

from Util import *
from PyQt4.QtCore import QObject, qDebug, SIGNAL

class Updater(QObject):
    DEFAULT_UPDATE_INTERVAL_SECS = 8
    ABSOLUTE_MINIMUM_UPDATE_INTERVAL_SECS = 5

    def __init__(self, throttledQuoter,
                 updateInterval=DEFAULT_UPDATE_INTERVAL_SECS):
        QObject.__init__(self)
        self.throttledQuoter = throttledQuoter
        self.stopped = False
        self.updateInterval = max(self.ABSOLUTE_MINIMUM_UPDATE_INTERVAL_SECS,
                                  updateInterval)
        self.currentUpdateInterval = self.updateInterval
        self.exchangeTickerTuples = []
        self.connect(self.throttledQuoter, SIGNAL("quotesCached"), self.quotesUpdated)

    def addTickers(self, tuple):
        self.exchangeTickerTuples.append(tuple)

    def start(self):
        self.tickersByExchange = self.groupTickersByExchange(self.exchangeTickerTuples)
        self.updateQuotes()
        self.timerId = self.startTimer(self.updateInterval * 1000)

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
        self.killTimer(self.timerId)

    def updateQuotes(self):
#        self.success = True
        for exchange in self.tickersByExchange.keys():
            qDebug("Getting quotes for exchange: %s" %(exchange))
            symbols = self.tickersByExchange[exchange]
            self.throttledQuoter.updateCache(exchange, symbols)
#            self.success = self.success & status

#        if self.success:
#            qDebug("[Updater] success")
#            self.currentUpdateInterval = max(self.currentUpdateInterval / 2, self.updateInterval)
#            self.emit(SIGNAL("quotesUpdated"))
#        else:
#            self.currentUpdateInterval = self.currentUpdateInterval * 2

        qDebug("[Updater] interval: %d" % (self.currentUpdateInterval))

    def quotesUpdated(self):
        self.emit(SIGNAL("quotesUpdated"))
