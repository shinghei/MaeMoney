from PyQt4.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant, QString
from Util import Util

class TransactionsModel(QAbstractTableModel):

    HEADERS = ["Type", "Date", "Shares @\nPrice", "Value +\nCommission"]
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

    def rowCount(self, parent = QModelIndex()):
        return len(self.transactions)

    def columnCount(self, parent = QModelIndex()):
        return len(self.HEADERS)

    def data(self,  index, role = Qt.DisplayRole ):

        row = index.row()
        col = index.column()

        if role == Qt.DisplayRole:

            transactData = self.transactions[row].transaction_data

            if col == self.COL_TYPE:
                return transactData.type

            elif col == self.COL_DATE:
                date = Util.extractDate(transactData.date)
                if date is None:
                    return "N/A"
                return date

            elif col == self.COL_SHARES_PRICE:
                return QString("%s @\n%s" %(transactData.shares, transactData.price.money[0].amount))

            elif col == self.COL_CASH_VALUE_COMMISSION:
                share = self.strToFloat(transactData.shares)
                price = self.strToFloat(transactData.price.money[0].amount)
                commission = self.strToFloat(transactData.commission.money[0].amount)
                currency = transactData.commission.money[0].currency_code
                cashValue = share * price + commission
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

    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.HEADERS[section]

    def strToFloat(self, s):
        try:
            return float(s)
        except ValueError:
            return None