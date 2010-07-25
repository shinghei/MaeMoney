from PyQt4.QtGui import QListView, QAbstractItemView, QMenu, QAction
from PyQt4 import QtCore
from PyQt4.QtCore import QEvent, SIGNAL, QObject, QPoint
from MaeMoneyProperties import MaeMoneyProperties

class PortfolioListView(QListView, QObject):

    def __init__(self, parent):
        '''
        @param parent - QMainWindow
        '''

        QListView.__init__(self, parent)

        self.parentWindow = parent
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.viewport().installEventFilter(self)

    def eventFilter(self, obj, event):
        '''
        @param obj QObject
        @paramn event QEvent
        '''

        #        if (event.type() == QEvent.MouseButtonPress):
        #            print "Mouse pressed"
        #
        if (event.type() == QEvent.ContextMenu):

            # Now we know that event is an instance of QContextMenuEvent

            menu = QMenu(self)

            newPos = self.adjustPosition(event.pos())
            modelIndex = self.indexAt(newPos)

            self.showTransactions = QAction(self.tr("Show transactions"), self)
            menu.addAction(self.showTransactions)
            self.connect(self.showTransactions,
                         SIGNAL("triggered()"),
                         lambda : self.parentWindow.showTransactionsForPosition(modelIndex))

            self.openWebpage = QAction(self.tr("Open Google Finance webpage"), self)
            menu.addAction(self.openWebpage)
            self.connect(self.openWebpage,
                         SIGNAL("triggered()"),
                         lambda : self.parentWindow.openWebpageForPosition(modelIndex))

            menu.exec_(event.globalPos())


        return QListView.eventFilter(self, obj, event)


    '''
    Due to a bug in PyQt on Maemo (or probably because I haven't yet figured out), the right clicked position
    is off.
    '''
    def adjustPosition(self, eventPos):
        '''
        @param eventPos - QPoint
        '''
        prop = MaeMoneyProperties.instance()

        newPos = QPoint(eventPos.x(), eventPos.y())
        if prop.isPortraitMode():
            offset = 50
        else:
            offset = 72

        newY = max(0, eventPos.y() - offset)
        newPos.setY(newY)


        return newPos

