from PyQt4.QtGui import QListView, QAbstractItemView, QMenu,  QAction
from PyQt4 import QtCore
from PyQt4.QtCore import QEvent

class PortfolioListView(QListView):

    def __init__(self, parent=None):
        QListView.__init__(self, parent)

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
            print "Right clicked!"
            menu = QMenu(self)

            menu.addAction(QAction("New",self))
            menu.exec_(event.globalPos())

        return QListView.eventFilter(self, obj, event)
