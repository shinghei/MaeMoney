from PyQt4.QtGui import QStyledItemDelegate, QFontMetrics, QLinearGradient, QFont, QPen, \
                        QStyle, QColor
from PyQt4.QtCore import QPointF, Qt, QRect, QSize

from PositionsModel import PositionsModel

class PositionsViewDelegate(QStyledItemDelegate):

    MARGIN = 5
    FONT_FAMILY = "Helvetica"
    MINIMUM_WIDTH = 320

    def __init__(self):
        QStyledItemDelegate.__init__(self)
        self.nameFont = self.configureTextFont(16, QFont.Normal)
        self.tickerFont = self.configureTextFont(14, QFont.Normal)
        self.currentPriceFont = self.configureTextFont(32, QFont.Bold)
        self.changeFont = self.configureTextFont(24, QFont.Normal)
        self.rightColFont = self.configureTextFont(14, QFont.Normal)

    def sizeHint(self, option, index):
        '''
        @param option  QStyleOptionViewItem
        @param index   QModelIndex
        '''

        textH = self.MARGIN + \
                QFontMetrics(self.nameFont).lineSpacing() + \
                self.MARGIN + \
                QFontMetrics(self.currentPriceFont).lineSpacing() + \
                self.MARGIN + \
                QFontMetrics(self.changeFont).lineSpacing() + \
                self.MARGIN

        hint = QSize(0, textH)

        return hint

    def createLinearGradient(self, itemRect, startColor, endColor):
        start = QPointF(itemRect.left(), itemRect.top())
        stop = QPointF(itemRect.right(), itemRect.bottom())
        linearGradient = QLinearGradient(start, stop)
        linearGradient.setColorAt(0, startColor)
        linearGradient.setColorAt(1, endColor)
        return linearGradient

    def paint (self, painter, option, index):

        painter.save()

        if option.state & QStyle.State_Selected:
            borderPen = QPen(Qt.blue)
            borderPen.setWidth(3)
            nameBgColors = [Qt.white, Qt.yellow]
        else:
            borderPen = QPen(Qt.lightGray)
            lightBlue = QColor(0, 0, 255).lighter(180)
            nameBgColors = [Qt.white, lightBlue]

        # Set default font and color
        itemRect = option.rect
        painter.fillRect(itemRect, Qt.white)
        painter.setFont(self.nameFont)
        painter.setPen(Qt.black)

        m = index.model()

        ticker = m.data(index, PositionsModel.ROLE_TICKER)
        companyName = m.data(index, Qt.DisplayRole)
        line2 = m.data(index, PositionsModel.ROLE_CURRENT_PRICE)
        line3 = m.data(index, PositionsModel.ROLE_CHANGE)

        fontMetricsCompanyName = QFontMetrics(self.nameFont)
        fontMetricsTicker = QFontMetrics(self.tickerFont)
        fontMetricsCurrentPrice = QFontMetrics(self.currentPriceFont)
        fontMetricsChange = QFontMetrics(self.changeFont)
        fontMetricsRightCol = QFontMetrics(self.rightColFont)
        lineSp1 = fontMetricsCompanyName.lineSpacing()
        lineSp2 = fontMetricsCurrentPrice.lineSpacing()
        lineSp3 = fontMetricsChange.lineSpacing()
        lineSpRightCol = fontMetricsRightCol.lineSpacing()

        # Company Name    (EXCHANGE:SYMBOL)
        textRectShade = QRect(itemRect.left(),
                              itemRect.top(),
                              itemRect.width(),
                              self.MARGIN + lineSp1 + self.MARGIN)
        gradient = self.createLinearGradient(textRectShade,
                                             nameBgColors[0],
                                             nameBgColors[1])
        painter.fillRect(textRectShade, gradient)
        textRect = QRect(itemRect.left() + self.MARGIN, itemRect.top() + self.MARGIN,
                         itemRect.width() - 2 * self.MARGIN, lineSp1 + self.MARGIN)
        painter.setFont(self.nameFont)
        # Shorten the company name such that long company names are not written on top of the ticker
        tickerTextW = fontMetricsTicker.width(ticker)
        companyNameTextW = textRect.width() - tickerTextW - self.MARGIN
        companyName = fontMetricsCompanyName.elidedText(companyName, Qt.ElideRight, companyNameTextW)
        painter.drawText(textRect, Qt.AlignVCenter | Qt.AlignLeft, companyName)
        painter.setFont(self.tickerFont)
        painter.drawText(textRect, Qt.AlignVCenter | Qt.AlignRight, "(%s)" % (ticker))

        # Current price
        painter.setFont(self.currentPriceFont)
        textRect.adjust(0, lineSp1 + self.MARGIN, 0, lineSp2 + self.MARGIN)
        painter.drawText(textRect, Qt.AlignTop | Qt.AlignLeft, line2)

        rightColRect = QRect(textRect.left(), textRect.top(),
                       textRect.width(), textRect.height())

        # Change
        ccol = m.data(index, PositionsModel.ROLE_CHANGE_COLOR)
        if ccol == "chg":
            painter.setPen(QPen(Qt.darkGreen))
        elif ccol == "chr":
            painter.setPen(QPen(Qt.red))
        painter.setFont(self.changeFont)
        textRect.adjust(0, lineSp2 + self.MARGIN, 0, lineSp3 + self.MARGIN)
        painter.drawText(textRect, Qt.AlignTop | Qt.AlignLeft, line3)

        ## Right column ##
        painter.setFont(self.rightColFont)
        painter.setPen(QPen(Qt.gray))
        # PE ratio
        pe = m.data(index, PositionsModel.ROLE_PE)
        painter.drawText(rightColRect, Qt.AlignTop | Qt.AlignRight, pe)
        # Market cap
        mktCap = m.data(index, PositionsModel.ROLE_MKT_CAP)
        rightColRect.adjust(0, lineSpRightCol, 0, 0)
        painter.drawText(rightColRect, Qt.AlignTop | Qt.AlignRight, mktCap)

        painter.setPen(borderPen)
        painter.drawRect(itemRect)

        painter.restore()

    def configureTextFont(self, fontSize, fontWeight = QFont.Normal):
        newTextFont = QFont(self.FONT_FAMILY)
        newTextFont.setWeight(fontWeight)
        newTextFont.setPointSize(fontSize)
        return newTextFont