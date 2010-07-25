from PyQt4.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant, QString, QObject
from TransactionDataWrapper import TransactionDataWrapper

class TransactionsModelLandscape(QAbstractTableModel):
    COL_TYPE = 0
    COL_DATE = 1
    COL_SHARES = 2
    COL_PRICE = 3
    COL_CASH_VALUE = 4
    COL_COMMISSION = 5

    '''
    @param transactions - list of TransactionData
    '''

    def __init__(self, transactions):
        QAbstractTableModel.__init__(self)
        self.transactions = transactions
        self.HEADERS = [self.tr("Type"),
                        self.tr("Date"),
                        self.tr("Shares"),
                        self.tr("Price"),
                        self.tr("Value"),
                        self.tr("Commission")]


    def rowCount(self, parent=QModelIndex()):
        return len(self.transactions)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADERS)

    def data(self, index, role=Qt.DisplayRole ):
        row = index.row()
        col = index.column()

        if role == Qt.DisplayRole:
            transactData = self.transactions[row].transaction_data
            transactDataWrapper = TransactionDataWrapper(transactData)

            if col == self.COL_TYPE:
                return transactDataWrapper.getType()

            elif col == self.COL_DATE:
                date = transactDataWrapper.getDate()
                if date is None:
                    return "N/A"
                return date

            elif col == self.COL_SHARES:
                shares = transactDataWrapper.getShares()
                return QString("%.0f" % (shares))

            elif col == self.COL_PRICE:
                unitPrice = transactDataWrapper.getUnitPrice()
                return QString("%.2f" % (unitPrice))

            elif col == self.COL_CASH_VALUE:
                shares = transactDataWrapper.getShares()
                unitPrice = transactDataWrapper.getUnitPrice()
                commission = transactDataWrapper.getCommission()
                cashValue = shares * unitPrice + commission
                return "%.2f" % (cashValue)

            elif col == self.COL_COMMISSION:
                commission = transactDataWrapper.getCommission()
                currency = transactDataWrapper.getCurrency()
                return "%s%.2f" % (currency, commission)

        elif role == Qt.TextAlignmentRole:
            if col == self.COL_TYPE or col == self.COL_DATE:
                return Qt.AlignLeft | Qt.AlignVCenter
            else:
                return Qt.AlignRight | Qt.AlignVCenter

        else:
            return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.HEADERS[section]
