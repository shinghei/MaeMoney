from PyQt4.QtGui import QStyledItemDelegate, QFontMetrics, QLinearGradient, QFont, QPen, \
                        QStyle, QColor
from PyQt4.QtCore import QPointF, Qt, QRect, QSize, QObject, QString

from PositionsModel import PositionsModel
from MaeMoneyProperties import MaeMoneyProperties

class PortraitSpecificDelegate(QObject):

    def __init__(self, viewDelegate):
        QObject.__init__(self)
        self.viewDelegate = viewDelegate
        self.nameFont = self.viewDelegate.configureTextFont(16, QFont.Normal)
        self.tickerFont = self.viewDelegate.configureTextFont(14, QFont.Normal)
        self.currentPriceFont = self.viewDelegate.configureTextFont(32, QFont.Bold)
        self.changeFont = self.viewDelegate.configureTextFont(24, QFont.Normal)
        self.rightColFont = self.viewDelegate.configureTextFont(14, QFont.Normal)
        self.fontMetricsRightCol = QFontMetrics(self.rightColFont)
        self.lineSpRightCol = self.fontMetricsRightCol.lineSpacing()

    def getNameFont(self):
        return self.nameFont

    def getTickerFont(self):
        return self.tickerFont

    def getCurrentPriceFont(self):
        return self.currentPriceFont

    def getChangeFont(self):
        return self.changeFont
        
    def sizeHint(self, option, index):
        '''
        Portrait mode - Left column
          Name (Symbol)
          --------------
          Current Price
          Change
        '''
        textHeightLCol = self.viewDelegate.MARGIN + \
                         QFontMetrics(self.nameFont).lineSpacing() + \
                         self.viewDelegate.MARGIN + \
                         QFontMetrics(self.currentPriceFont).lineSpacing() + \
                         self.viewDelegate.MARGIN + \
                         QFontMetrics(self.changeFont).lineSpacing() + \
                         self.viewDelegate.MARGIN

        '''
        Portrait mode - Right column
          Name (Symbol)
          --------------
          PE ratio
          Market Cap
          Daily volume
          Average volume
          Delay
        '''
        textHeightRCol = self.viewDelegate.MARGIN_RCOL + \
                         QFontMetrics(self.nameFont).lineSpacing() + \
                         self.viewDelegate.MARGIN_RCOL + \
                         QFontMetrics(self.rightColFont).lineSpacing() + \
                         self.viewDelegate.MARGIN_RCOL + \
                         QFontMetrics(self.rightColFont).lineSpacing() + \
                         self.viewDelegate.MARGIN_RCOL + \
                         QFontMetrics(self.rightColFont).lineSpacing() + \
                         self.viewDelegate.MARGIN_RCOL + \
                         QFontMetrics(self.rightColFont).lineSpacing() + \
                         self.viewDelegate.MARGIN_RCOL + \
                         QFontMetrics(self.rightColFont).lineSpacing() + \
                         self.viewDelegate.MARGIN

        hint = QSize(0, max(textHeightLCol, textHeightRCol))
        return hint

    def paintRightCol(self, index, painter, rightColRect):
        '''
        @param QModelIndex index
        @param QPainter painter
        @param QRect rightColRect
        '''
        
        painter.setFont(self.rightColFont)
        painter.setPen(QPen(Qt.gray))

        m = index.model()
        lineSp = self.lineSpRightCol + self.viewDelegate.MARGIN_RCOL

        # PE ratio
        pe = m.data(index, PositionsModel.ROLE_PE)
        peStr = self.tr("PE ratio: ") + pe
        painter.drawText(rightColRect, Qt.AlignTop | Qt.AlignRight, peStr)
        # Market cap
        mktCap = m.data(index, PositionsModel.ROLE_MKT_CAP)
        mktCapStr = self.tr("Mkt Cap: ") + mktCap
        rightColRect.adjust(0, lineSp, 0, lineSp)
        painter.drawText(rightColRect, Qt.AlignTop | Qt.AlignRight, mktCapStr)
        # Daily Volume
        vol = m.data(index, PositionsModel.ROLE_DAILY_VOL)
        volStr = self.tr("Vol: ") + QString(vol)
        rightColRect.adjust(0, lineSp, 0, lineSp)
        painter.drawText(rightColRect, Qt.AlignTop | Qt.AlignRight, volStr)
        # Average Volume
        avgVol = m.data(index, PositionsModel.ROLE_AVG_VOL)
        avgVolStr = self.tr("Avg Vol: ") + QString(avgVol)
        rightColRect.adjust(0, lineSp, 0, lineSp)
        painter.drawText(rightColRect, Qt.AlignTop | Qt.AlignRight, avgVolStr)
        # Delay
        delay = m.data(index, PositionsModel.ROLE_DELAY)
        if delay == "":
            delayStr = self.tr("Realtime data")
        else:
            delayStr = self.tr("Delay: ") + delay + self.tr(" mins")
        rightColRect.adjust(0, lineSp, 0, lineSp)
        painter.drawText(rightColRect, Qt.AlignTop | Qt.AlignRight, delayStr)


class LandscapeSpecificDelegate(QObject):

    def __init__(self, viewDelegate):
        QObject.__init__(self)
        self.viewDelegate = viewDelegate
        self.nameFont = self.viewDelegate.configureTextFont(16, QFont.Normal)
        self.tickerFont = self.viewDelegate.configureTextFont(14, QFont.Normal)
        self.currentPriceFont = self.viewDelegate.configureTextFont(32, QFont.Bold)
        self.changeFont = self.viewDelegate.configureTextFont(24, QFont.Normal)
        self.rightColFont = self.viewDelegate.configureTextFont(14, QFont.Normal)
        self.fontMetricsRightCol = QFontMetrics(self.rightColFont)
        self.lineSpRightCol = self.fontMetricsRightCol.lineSpacing()

    def sizeHint(self, option, index):
        textH = self.viewDelegate.MARGIN + \
                QFontMetrics(self.nameFont).lineSpacing() + \
                self.viewDelegate.MARGIN + \
                QFontMetrics(self.currentPriceFont).lineSpacing() + \
                self.viewDelegate.MARGIN + \
                QFontMetrics(self.changeFont).lineSpacing() + \
                self.viewDelegate.MARGIN

        hint = QSize(0, textH)
        return hint

    def getNameFont(self):
        return self.nameFont

    def getTickerFont(self):
        return self.tickerFont

    def getCurrentPriceFont(self):
        return self.currentPriceFont

    def getChangeFont(self):
        return self.changeFont

    def paintRightCol(self, index, painter, rightColRect):
        '''
        @param QModelIndex index
        @param QPainter painter
        @param QRect rightColRect
        '''

        painter.setFont(self.rightColFont)
        painter.setPen(QPen(Qt.gray))

        m = index.model()
        lineSp = self.lineSpRightCol + self.viewDelegate.MARGIN_RCOL

        # PE ratio
        pe = m.data(index, PositionsModel.ROLE_PE)
        peStr = self.tr("P/E ratio: ") + pe
        painter.drawText(rightColRect, Qt.AlignTop | Qt.AlignRight, peStr)
        # Market cap
        mktCap = m.data(index, PositionsModel.ROLE_MKT_CAP)
        mktCapStr = self.tr("Market Cap.: ") + mktCap
        rightColRect.adjust(0, lineSp, 0, lineSp)
        painter.drawText(rightColRect, Qt.AlignTop | Qt.AlignRight, mktCapStr)
        # Daily Volume / Average Volume
        vol = m.data(index, PositionsModel.ROLE_DAILY_VOL)
        avgVol = m.data(index, PositionsModel.ROLE_AVG_VOL)
        volAvgVolStr = self.tr("Daily / Avg Vol.: ") + QString(vol) + "/" + QString(avgVol)
        rightColRect.adjust(0, lineSp, 0, lineSp)
        painter.drawText(rightColRect, Qt.AlignTop | Qt.AlignRight, volAvgVolStr)
        # Delay
        delay = m.data(index, PositionsModel.ROLE_DELAY)
        if delay == "":
            delayStr = self.tr("Realtime data")
        else:
            delayStr = self.tr("Delay: ") + delay + self.tr(" minutes")
        rightColRect.adjust(0, lineSp, 0, lineSp)
        painter.drawText(rightColRect, Qt.AlignTop | Qt.AlignRight, delayStr)

class PositionsViewDelegate(QStyledItemDelegate):
    MARGIN = 5
    MARGIN_RCOL = 2
    FONT_FAMILY = "Helvetica"
    MINIMUM_WIDTH = 320

    def __init__(self):
        QStyledItemDelegate.__init__(self)
        self.prop = MaeMoneyProperties.instance()
        self.portraitSpecificDelegate = PortraitSpecificDelegate(self)
        self.landscapeSpecificDelegate = LandscapeSpecificDelegate(self)

    def sizeHint(self, option, index):
        '''
        @param option  QStyleOptionViewItem
        @param index   QModelIndex
        '''
        orntnDelegate = self.chooseOrientationDelegate()
        return orntnDelegate.sizeHint(option, index)

    def createLinearGradient(self, itemRect, startColor, endColor):
        start = QPointF(itemRect.left(), itemRect.top())
        stop = QPointF(itemRect.right(), itemRect.bottom())
        linearGradient = QLinearGradient(start, stop)
        linearGradient.setColorAt(0, startColor)
        linearGradient.setColorAt(1, endColor)
        return linearGradient

    def paint (self, painter, option, index):
        '''
        QPainter * painter, const QStyleOptionViewItem & option, const QModelIndex & index
        '''

        orntnDelegate = self.chooseOrientationDelegate()
        
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
        painter.setFont(orntnDelegate.getNameFont())
        painter.setPen(Qt.black)

        m = index.model()

        ticker = m.data(index, PositionsModel.ROLE_TICKER)
        companyName = m.data(index, Qt.DisplayRole)
        line2 = m.data(index, PositionsModel.ROLE_CURRENT_PRICE)
        line3 = m.data(index, PositionsModel.ROLE_CHANGE)

        fontMetricsCompanyName = QFontMetrics(orntnDelegate.getNameFont())
        fontMetricsTicker = QFontMetrics(orntnDelegate.getTickerFont())
        fontMetricsCurrentPrice = QFontMetrics(orntnDelegate.getCurrentPriceFont())
        fontMetricsChange = QFontMetrics(orntnDelegate.getChangeFont())
        lineSp1 = fontMetricsCompanyName.lineSpacing()
        lineSp2 = fontMetricsCurrentPrice.lineSpacing()
        lineSp3 = fontMetricsChange.lineSpacing()

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
        painter.setFont(orntnDelegate.getNameFont())
        # Shorten the company name such that long company names are not written on top of the ticker
        tickerTextW = fontMetricsTicker.width(ticker)
        companyNameTextW = textRect.width() - tickerTextW - 2 * self.MARGIN
        companyName = fontMetricsCompanyName.elidedText(companyName, Qt.ElideRight, companyNameTextW)
        painter.drawText(textRect, Qt.AlignVCenter | Qt.AlignLeft, companyName)
        painter.setFont(orntnDelegate.getTickerFont())
        painter.drawText(textRect, Qt.AlignVCenter | Qt.AlignRight, "(%s)" % (ticker))

        # Current price
        painter.setFont(orntnDelegate.getCurrentPriceFont())
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
        painter.setFont(orntnDelegate.getChangeFont())
        textRect.adjust(0, lineSp2 + self.MARGIN, 0, lineSp3 + self.MARGIN)
        painter.drawText(textRect, Qt.AlignTop | Qt.AlignLeft, line3)

        '''
        Right Column
        '''

        orntnDelegate.paintRightCol(index, painter, rightColRect)

        painter.setPen(borderPen)
        painter.drawRect(itemRect)

        painter.restore()

    def configureTextFont(self, fontSize, fontWeight=QFont.Normal):
        newTextFont = QFont(self.FONT_FAMILY)
        newTextFont.setWeight(fontWeight)
        newTextFont.setPointSize(fontSize)
        return newTextFont

    def chooseOrientationDelegate(self):
        if self.prop.isPortraitMode():
            return self.portraitSpecificDelegate
        else:
            return self.landscapeSpecificDelegate