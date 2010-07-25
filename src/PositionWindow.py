from PyQt4.QtGui import QMainWindow, QTableView, QWidget, QVBoxLayout, QHeaderView, QAbstractItemView
from MaeMoneyProperties import MaeMoneyProperties
from PyQt4.QtCore import qDebug

class PositionWindow(QMainWindow):

    WA_Maemo5StackedWindow = 127
    WA_Maemo5PortraitOrientation = 128
    WA_Maemo5LandscapeOrientation = 129

    '''
    @param transactionModel - TransactionModel
    '''
    def __init__(self, parent, exchange, ticker, transactionModel):
        QMainWindow.__init__(self, parent)

        self.prop = MaeMoneyProperties.instance()
        self.setupUi(exchange, ticker, transactionModel)

    def setupUi(self, exchange, ticker, transactionModel):

        self.setWindowTitle("%s:%s" %(exchange, ticker))
        widget = QWidget(self)
        self.setCentralWidget(widget)

        self.layout = QVBoxLayout()
        widget.setLayout(self.layout)

        self.transactTableView = QTableView(self)
        self.transactTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        header = self.transactTableView.horizontalHeader()
        header.setResizeMode(QHeaderView.ResizeToContents)
        self.transactTableView.setHorizontalHeader(header)
        self.transactTableView.setModel(transactionModel)
        self.transactTableView.resizeRowsToContents()
        self.transactTableView.resizeColumnsToContents()
        header.setStretchLastSection(True)
        self.layout.addWidget(self.transactTableView)

        self.setOrientation()
        self.setAttributeAndCatch(self.WA_Maemo5StackedWindow, True)

    def setAttributeAndCatch(self, attribute, trueFalse):
        try:
            self.setAttribute(attribute, trueFalse)
        except AttributeError:
            qDebug("Can't set attribute %d" %(attribute))

    def setOrientation(self):
        if self.prop.isPortraitMode():
            self.setAttributeAndCatch(self.WA_Maemo5PortraitOrientation, True)
            self.setAttributeAndCatch(self.WA_Maemo5LandscapeOrientation, False)
        else:
            self.setAttributeAndCatch(self.WA_Maemo5LandscapeOrientation, True)
            self.setAttributeAndCatch(self.WA_Maemo5PortraitOrientation, False)
