# coding=utf-8

from PyQt4.QtCore import QAbstractTableModel, QVariant, Qt
from PyQt4.QtGui import QColor, QBrush
import string

class PortfolioTableModel(QAbstractTableModel):

    COL_NAME = 0
    COL_PRICE = 1
    COL_CHANGE = 2
    COL_MKT_CAP = 3

    ROLE_SUBTEXT1 = Qt.UserRole + 1
    ROLE_COLOR = ROLE_SUBTEXT1 + 1

    def __init__(self, inputArray, headerData, rtQuoter, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.inputArray = inputArray
        self.headerData = headerData
        self.rtQuoter = rtQuoter

    def rowCount(self, parent):
        return len(self.inputArray)

    def columnCount(self, parent): 
        return len(self.headerData)

    def data(self, index, role):

        if index.isValid():
            
            exchange = self.getExchange(index)
            ticker = self.getTicker(index)

            if role == Qt.DisplayRole:

                if index.column() is self.COL_NAME:
                    return "%s:%s" %(exchange, ticker)

                elif index.column() is self.COL_CHANGE:
                    return self.rtQuoter.getChange(exchange, ticker)

                elif index.column() is self.COL_PRICE:
                    return self.rtQuoter.getPrice(exchange, ticker)

                elif index.column() is self.COL_MKT_CAP:
                    return self.rtQuoter.getMarketCap(exchange, ticker)

            elif role == self.ROLE_SUBTEXT1:
                if index.column() is self.COL_NAME:
                    return self.rtQuoter.getFullName(exchange, ticker)

                elif index.column() is self.COL_CHANGE:
                    changePct = self.rtQuoter.getChangePercentage(exchange, ticker)
                    if changePct is not None:
                        changePct = "(%s)" %(changePct + '%')
                    return changePct

            elif role == self.ROLE_COLOR:
                return self.rtQuoter.getColor(exchange, ticker)

        return QVariant()

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerData[col])
        return QVariant()

    def getExchange(self, index):
        exchange = self.inputArray[index.row()]['exchange']
        return exchange

    def getTicker(self, index):
        ticker = self.inputArray[index.row()]['ticker']
        return ticker
