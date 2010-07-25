from PyQt4.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant, QString, QObject
from TransactionDataWrapper import TransactionDataWrapper

class TransactionsModelPortrait(QAbstractTableModel):
    COL_TYPE = 0
    COL_DATE = 1
    COL_SHARES_PRICE = 2
    COL_CASH_VALUE_COMMISSION = 3

    '''
    @param transactions - list of TransactionData
    '''

    def __init__(self, transactions):
        QAbstractTableModel.__init__(self)
        self.transactions = transactions
        self.HEADERS = [self.tr("Type"),
                        self.tr("Date"),
                        self.tr("Shares @\nPrice"),
                        self.tr("Value +\nCommission")]


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

            elif col == self.COL_SHARES_PRICE:
                shares = transactDataWrapper.getShares()
                unitPrice = transactDataWrapper.getUnitPrice()
                return QString("%.0f @\n%.2f" % (shares, unitPrice))

            elif col == self.COL_CASH_VALUE_COMMISSION:
                shares = transactDataWrapper.getShares()
                unitPrice = transactDataWrapper.getUnitPrice()
                commission = transactDataWrapper.getCommission()
                currency = transactDataWrapper.getCurrency()
                cashValue = shares * unitPrice + commission
                return "%.2f\n+ %s%.2f" % (cashValue, currency, commission)

        elif role == Qt.TextAlignmentRole:
            if col == self.COL_TYPE:
                return Qt.AlignLeft | Qt.AlignVCenter

            elif col == self.COL_DATE:
                return Qt.AlignLeft | Qt.AlignVCenter

            elif col == self.COL_SHARES_PRICE:
                return Qt.AlignRight | Qt.AlignVCenter

            elif col == self.COL_CASH_VALUE_COMMISSION:
                return Qt.AlignRight | Qt.AlignVCenter

        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.HEADERS[section]
