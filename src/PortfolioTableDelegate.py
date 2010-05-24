from PyQt4.QtGui import QStyledItemDelegate, QFont, QStyleOptionViewItemV4, \
                        QPalette, QPen, QStyle, QConicalGradient, QLinearGradient, \
                        QFontMetrics
from PyQt4.QtCore import QRect, QSize, QPointF, qWarning
from PortfolioTableModel import *

class PortfolioTableDelegate(QStyledItemDelegate):

    MARGIN = 10

    def sizeHint(self, option, index):
        '''
        @param option  QStyleOptionViewItem
        @param index   QModelIndex
        '''

        line1 = index.data(Qt.DisplayRole).toString()
        line2 = index.data(PortfolioTableModel.ROLE_SUBTEXT1).toString()
        textW1 = option.fontMetrics.width(line1)
        textW2 = option.fontMetrics.width(line2)
        textW = max(textW1, textW2)
        textH = option.fontMetrics.lineSpacing()

        numLines = 2

        hint = QSize(textW + 2 * self.MARGIN, numLines * textH + 2 * self.MARGIN)

        return hint

    def createLinearGradient(self, itemRect, startColor, endColor):
        start = QPointF(itemRect.left(), itemRect.top())
        stop = QPointF(itemRect.right(), itemRect.bottom())
        linearGradient = QLinearGradient(start, stop)
        linearGradient.setColorAt(0, startColor)
        linearGradient.setColorAt(1, endColor)
        return linearGradient

    def subTextFont(self, currentPainterFont, decrement):
        subTextFont = QFont()
        subTextFont.setWeight(QFont.Light)
        subTextFont.setPointSize(currentPainterFont.pointSize() - decrement)
        return subTextFont

    def paint (self, painter, option, index):
        '''
        @param painter QPainter
        @param option  QStyleOptionViewItem
        @param index   QModelIndex
        '''

        if index.column() is PortfolioTableModel.COL_NAME:
           
            painter.save()
            painter.setPen(QPen(option.palette.color(QPalette.Text)))

            m = index.model()
            line1 = m.data(index, Qt.DisplayRole)
            line2 = m.data(index, PortfolioTableModel.ROLE_SUBTEXT1)

            itemRect = option.rect

            if option.state & QStyle.State_Selected:
                painter.fillRect(itemRect, Qt.darkRed)
                highlighted = painter.pen()
                highlighted.setColor(Qt.yellow)
                painter.setPen(highlighted)
            else:
                linearGradient = self.createLinearGradient(itemRect, Qt.white, Qt.gray)
                painter.fillRect(itemRect, linearGradient)

            lineSp = option.fontMetrics.lineSpacing()
            numLines = 2
            subTextColor = painter.pen().color()
            subTextColor.setAlphaF(0.5)
            subTextFont = self.subTextFont(painter.font(), 2)

            textRect = QRect(itemRect.left() + self.MARGIN, itemRect.top() + self.MARGIN,
                             itemRect.width() - self.MARGIN, numLines * lineSp)
            painter.drawText(textRect, Qt.AlignTop | Qt.AlignLeft, line1)

            if line2 is not None:
                textRect.adjust(0, option.fontMetrics.lineSpacing(), 0, 0)
                painter.setPen(subTextColor)
                painter.setFont(subTextFont)
                painter.drawText(textRect, Qt.AlignTop | Qt.AlignLeft, line2)
            else:
                qWarning("Company name is null.")


            painter.restore()

        elif index.column() is PortfolioTableModel.COL_PRICE:

            painter.save()
            painter.setPen(QPen(option.palette.color(QPalette.Text)))

            itemRect = option.rect

            m = index.model()

            line = m.data(index, Qt.DisplayRole)

            if option.state & QStyle.State_Selected:
                painter.fillRect(itemRect, Qt.darkRed)
                highlighted = painter.pen()
                highlighted.setColor(Qt.yellow)
                painter.setPen(highlighted)
            else:
                color = m.data(index, PortfolioTableModel.ROLE_COLOR)
                if color ==  "chg":
                    painter.fillRect(itemRect, Qt.darkGreen)
                elif color == "chr":
                    painter.fillRect(itemRect, Qt.red)
                else:
                    painter.fillRect(itemRect, Qt.darkGray)

                pen = painter.pen()
                pen.setColor(Qt.white)
                painter.setPen(pen)

            lineSp = option.fontMetrics.lineSpacing()
                
            textRect = QRect(itemRect.left() + self.MARGIN, itemRect.top() + self.MARGIN,
                             itemRect.width() - self.MARGIN, lineSp)
            painter.drawText(textRect, Qt.AlignTop | Qt.AlignRight, line)

            painter.restore()

        elif index.column() is PortfolioTableModel.COL_CHANGE:

            painter.save()
            painter.setPen(QPen(option.palette.color(QPalette.Text)))

            itemRect = option.rect

            m = index.model()

            line1 = m.data(index, Qt.DisplayRole)
            line2 = m.data(index, PortfolioTableModel.ROLE_SUBTEXT1)

            if option.state & QStyle.State_Selected:
                painter.fillRect(itemRect, Qt.darkRed)
                highlighted = painter.pen()
                highlighted.setColor(Qt.yellow)
                painter.setPen(highlighted)
            else:
                linearGradient = self.createLinearGradient(itemRect, Qt.white, Qt.darkYellow)
                painter.fillRect(itemRect, linearGradient)

            color = m.data(index, PortfolioTableModel.ROLE_COLOR)
            if color ==  "chg":
                painter.setPen(Qt.darkGreen)
            elif color == "chr":
                painter.setPen(Qt.red)

            lineSp = option.fontMetrics.lineSpacing()
            numLines = 2

            textRect = QRect(itemRect.left(), itemRect.top() + self.MARGIN,
                             itemRect.width() - self.MARGIN, numLines * lineSp)
            painter.drawText(textRect, Qt.AlignTop | Qt.AlignHCenter, line1)

            textRect.adjust(0, option.fontMetrics.lineSpacing(), 0, 0)
            painter.drawText(textRect, Qt.AlignTop | Qt.AlignHCenter, line2)

            painter.restore()

        else:
            QStyledItemDelegate.paint(self, painter, option, index)


#            painter.setPen(QPen(option.palette.color(QPalette.HighlightedText)))
#        else:
#            painter.setPen(QPen(option.palette.color(QPalette.Text)))

