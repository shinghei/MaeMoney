from PyQt4.QtCore import QAbstractListModel
from PyQt4.QtCore import Qt, QVariant, qDebug, SIGNAL, QModelIndex, QString
import PyQt4.QtGui

class PositionsModel(QAbstractListModel):

    ROLE_CURRENT_PRICE = Qt.UserRole + 1
    ROLE_CHANGE        = Qt.UserRole + 2
    ROLE_TICKER        = Qt.UserRole + 3
    ROLE_CHANGE_COLOR  = Qt.UserRole + 4
    ROLE_MKT_CAP       = Qt.UserRole + 5
    ROLE_PE            = Qt.UserRole + 6
    ROLE_DELAY         = Qt.UserRole + 7
    ROLE_DAILY_VOL     = Qt.UserRole + 8
    ROLE_AVG_VOL       = Qt.UserRole + 9

    def __init__(self, inputArray, quoter, parent=None, *args):
        QAbstractListModel.__init__(self, parent, *args)
        self.inputArray = inputArray
        self.quoter = quoter

    def rowCount(self, parent = QModelIndex()):
        return len(self.inputArray)

    def data(self, index, role = Qt.DisplayRole):

        exchange = self.getExchange(index)
        ticker = self.getTicker(index)

        if role == Qt.DisplayRole:
            name = self.quoter.getFullName(exchange, ticker)
            return name

        elif role == self.ROLE_TICKER:
            exchTicker = "%s:%s" %(exchange, ticker)
            return exchTicker

        elif role == self.ROLE_CURRENT_PRICE:
            price = self.quoter.getPrice(exchange, ticker)
            return price

        elif role == self.ROLE_CHANGE:
            change = self.quoter.getChange(exchange, ticker)
            changePct = self.quoter.getChangePercentage(exchange, ticker)
            if change is not None and changePct is not None:
                return "%s (%s)" % (change, changePct + '%')
            return ""

        elif role == self.ROLE_CHANGE_COLOR:
            return self.quoter.getColor(exchange, ticker)

        elif role == self.ROLE_MKT_CAP:
            mktCap = self.quoter.getMarketCap(exchange, ticker)
            return mktCap

        elif role == self.ROLE_PE:
            peRatio = self.quoter.getPeRatio(exchange, ticker)
            return peRatio

        elif role == self.ROLE_DELAY:
            delay = self.quoter.getDelay(exchange, ticker)
            return delay

        elif role == self.ROLE_DAILY_VOL:
            vol = self.quoter.getVolume(exchange, ticker)
            if vol is not None:
                return vol
            return ""

        elif role == self.ROLE_AVG_VOL:
            avgVol = self.quoter.getAverageVolume(exchange, ticker)
            if avgVol is not None:
                return avgVol
            return ""

        else:
            return QVariant()

    def getExchange(self, index):
        exchange = self.inputArray[index.row()]['exchange']
        return exchange

    def getTicker(self, index):
        ticker = self.inputArray[index.row()]['ticker']
        return ticker

    def emitModelReset(self):

        for i in range(self.rowCount()):
            index = self.createIndex(i, 0)
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                             index,
                             index)