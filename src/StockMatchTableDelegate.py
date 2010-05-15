from PyQt4.QtCore import QRect, QSize, QPointF
from PyQt4.QtGui import QFont, QStyledItemDelegate, QStyleOptionViewItemV4, \
                        QLinearGradient, QStyle

from StockMatchWin import *
from StockMatchTableModel import *

class StockMatchTableDelegate(QStyledItemDelegate):

    MARGIN = 10

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

    def sizeHint(self, option, index):
        line1 = index.data(Qt.DisplayRole).toString()

        textW = option.fontMetrics.width(line1)

        lineSpacing = option.fontMetrics.lineSpacing()
        numLines = 2
        delta = self.MARGIN
        hint = QSize(textW + delta, numLines * lineSpacing + delta)

        return hint

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

        if index.column() is StockMatchTableModel.COL_TICKER:

            painter.save()

            m = index.model()
            line1 = m.data(index, Qt.DisplayRole).toString()

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
            textRect = QRect(itemRect.left() + leftMargin, itemRect.bottom() - numLines * lineSp,
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