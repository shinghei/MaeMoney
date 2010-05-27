from PyQt4.QtCore import QRect, QSize, QPointF
from PyQt4.QtGui import QFont, QStyledItemDelegate, QStyleOptionViewItemV4, \
                        QLinearGradient, QStyle

from StockMatchWin import *
from StockMatchTableModel import *

class StockMatchTableDelegate(QStyledItemDelegate):

    MARGIN = 5

    def __init__(self):
        QStyledItemDelegate.__init__(self)
        self.columnWidths = {}
        self.columnWidths[StockMatchTableModel.COL_TICKER] = 150
        self.columnWidths[StockMatchTableModel.COL_NAME] = 400

    def sizeHint(self, option, index):

        textW = self.columnWidths[index.column()]

        lineSpacing = option.fontMetrics.lineSpacing()
        numLines = 2
        delta = self.MARGIN

        hint = QSize(delta + textW + delta, delta + numLines * lineSpacing + delta)
        return hint

    def createLinearGradient(self, itemRect, startColor, endColor):
        '''
        Creates linear gradient starting from top left to bottom right
        '''
        start = QPointF(itemRect.left(), itemRect.top())
        stop = QPointF(itemRect.right(), itemRect.bottom())
        linearGradient = QLinearGradient(start, stop)
        linearGradient.setColorAt(0, startColor)
        linearGradient.setColorAt(1, endColor)
        return linearGradient

    def setPenColor(self, painter, color):
        highlighted = painter.pen()
        highlighted.setColor(color)
        painter.setPen(highlighted)

    def paint (self, painter, option, index):
        '''
        @param painter QPainter
        @param option    QStyleOptionViewItem
        @param index   QModelIndex
        '''

        itemRect = option.rect

        textW = self.columnWidths[index.column()]

        if index.column() is StockMatchTableModel.COL_TICKER:

            painter.save()

            m = index.model()
            line1 = m.data(index, Qt.DisplayRole).toString()
            line1 = option.fontMetrics.elidedText(line1, Qt.ElideLeft, textW)           

            # Paint the background first and then set the pen color
            if option.state & QStyle.State_Selected:
                painter.fillRect(itemRect, Qt.white)
                self.setPenColor(painter, Qt.darkBlue)
            else:
                linearGradient = self.createLinearGradient(itemRect, Qt.black, Qt.blue)
                painter.fillRect(itemRect, linearGradient)
                self.setPenColor(painter, Qt.white)

            textRect = itemRect
            painter.drawText(textRect, Qt.AlignVCenter | Qt.AlignCenter, line1)

            painter.restore()

        elif index.column() is StockMatchTableModel.COL_NAME:
           # Name column
            
            painter.save()

            m = index.model()
            line1 = m.data(index, Qt.DisplayRole).toString()
            line1 = option.fontMetrics.elidedText(line1, Qt.ElideRight, textW)
            line2 = m.data(index, StockMatchTableModel.ROLE_SUBTEXT1).toString()

            # Paint the background first and then set the pen color
            if option.state & QStyle.State_Selected:
                linearGradient = self.createLinearGradient(itemRect, Qt.white, Qt.yellow)
                painter.fillRect(itemRect, linearGradient)
                self.setPenColor(painter, Qt.darkBlue)
            else:
                linearGradient = self.createLinearGradient(itemRect, Qt.blue, Qt.darkBlue)
                painter.fillRect(itemRect, linearGradient)
                self.setPenColor(painter, Qt.white)

            lineSp = option.fontMetrics.lineSpacing()
            numLines = 2

            leftMargin = self.MARGIN
            textRect = QRect(itemRect.left() + leftMargin, itemRect.top() + self.MARGIN,
                             itemRect.width(), numLines * lineSp)
            painter.drawText(textRect, Qt.AlignTop | Qt.AlignLeft, line1)

            textRect.adjust(0, option.fontMetrics.lineSpacing(), 0, 0)

            # Draw the subtext
            subTextColor = painter.pen().color()
            subTextColor.setAlphaF(0.5)
            painter.setPen(subTextColor)
            painter.drawText(textRect, Qt.AlignTop | Qt.AlignLeft, line2)


            painter.restore()
        else:
            QStyledItemDelegate.paint(self, painter, option, index)