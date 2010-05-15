from PyQt4.Qt import QListView, Qt, QAbstractItemView, QMenu, QMenu, QEvent, QEvent, QAction

class PortfolioListView(QListView):

    def __init__(self, parent=None):
        QListView.__init__(self, parent)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
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
