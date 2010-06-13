from PyQt4.QtCore import QAbstractListModel, QVariant, QString, Qt, QTextCodec

class PortfolioListModel(QAbstractListModel):

    def __init__(self, portfolios, parent=None, *args):
        QAbstractListModel.__init__(self, parent, *args)
        self.portfolios = portfolios

    def rowCount(self, parent):
        return len(self.portfolios)

    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            rawText = self.portfolios[index.row()].title.text
            return rawText.decode("utf-8")
        else:
            return QVariant()

    def getPortfolio(self, qModelIndex):
        return self.portfolios[qModelIndex.row()]

    def getPortfolioByRow(self, row):
        return self.portfolios[row]