# coding=utf-8

from PyQt4.QtCore import Qt, QVariant, QModelIndex, QAbstractTableModel, qWarning

class StockMatchTableModel(QAbstractTableModel):
    HEADER = ["Ticker", "Name"]
    COL_TICKER = 0
    COL_NAME = 1

    ROLE_SUBTEXT1 = Qt.UserRole + 1

    # http://www.wikinvest.com/wiki/List_of_Stock_Exchanges
    COUNTRY_CN = u'中国'
    COUNTRY_HK = u'香港'
    COUNTRY_US = u'United States'

    COUNTRY_AUSTRALIA = u'Australia'
    COUNTRY_INDIA = u'भारत गणराज्य'
    COUNTRY_INDONESIA = u'Republik Indonesia'
    COUNTRY_JAPAN = u'日本'
    COUNTRY_KOREA = u'한국'
    COUNTRY_MALAYSIA = u'Malaysia'
    COUNTRY_NEW_ZEALAND = u'New Zealand'
    COUNTRY_PAKISTAN = u'پاکِستان'
    COUNTRY_PHILIPPINES = u'Pilipinas'
    COUNTRY_SINGAPORE = u'Singapore'
    COUNTRY_SRI_LANKA = u'Sri Lanka'
    COUNTRY_TAIWAN = u'臺灣'
    COUNTRY_THAILAND = u'ราชอาณาจักรไทย'
    COUNTRY_AUSTRIA = u'Republik Österreich'
    COUNTRY_BELGIUM = u'Belgium'
    COUNTRY_BULGARIA = u'България'
    COUNTRY_CROATIA = u'Croatia'
    COUNTRY_CYPRUS = u'Cyprus'
    COUNTRY_CZECH_REPUBLIC = u'Czech Republic'
    COUNTRY_DENMARK = u'Denmark'
    COUNTRY_ESTONIA = u'Estonia'
    COUNTRY_FINLAND = u'Suomen tasavalta'
    COUNTRY_FRANCE = u'République française'
    COUNTRY_GERMANY = u'Bundesrepublik Deutschland'
    COUNTRY_GREECE = u'Ελληνική Δημοκρατία'
    COUNTRY_HOLLAND = u'Holland'
    COUNTRY_HUNGARY = u'Magyar Köztársaság'
    COUNTRY_IRELAND = u'Ireland'
    COUNTRY_ITALTY = u'Repubblica italiana'
    COUNTRY_LATVIA = u'Latvijas Republika'
    COUNTRY_LITHUANIA = u'Lietuvos Respublika'
    COUNTRY_LUXEMBOURG = u'Groussherzogtum Lëtzebuerg'
    COUNTRY_MACEDONIA = u'Republic of Macedonia'
    COUNTRY_NORWAY = u'Norway'
    COUNTRY_POLAND = u'Rzeczpospolita Polska'
    COUNTRY_PORTUGAL = u'República Portuguesa'
    COUNTRY_ROMANIA = u'România'
    COUNTRY_RUSSIA = u'Российская Федерация'
    COUNTRY_SLOVENIA = u'Republika Slovenija'
    COUNTRY_SPAIN = u'Reino de España'
    COUNTRY_SWEDEN = u'Konungariket Sverige'
    COUNTRY_SWITZERLAND = u'Switzerland'
    COUNTRY_TURKEY = u'Türkiye Cumhuriyeti'
    COUNTRY_UK = u'UK'

    COUNTRY_UNKNOWN = 'Unknown'
    countryExchangeMap = {'ASX': COUNTRY_AUSTRALIA,
                          'NSE': COUNTRY_INDIA,
                          'BOM': COUNTRY_INDIA,
                          'JAK': COUNTRY_INDONESIA,
                          'FUK': COUNTRY_JAPAN,
                          'NJM': COUNTRY_JAPAN,
                          'JSD': COUNTRY_JAPAN,
                          'NAG': COUNTRY_JAPAN,
                          'OSA': COUNTRY_JAPAN,
                          'TYO': COUNTRY_JAPAN,
                          'SEO': COUNTRY_KOREA,
                          'KDQ': COUNTRY_KOREA,
                          'KUL': COUNTRY_MALAYSIA,
                          'NZE': COUNTRY_NEW_ZEALAND,
                          'KAR': COUNTRY_PAKISTAN,
                          'Lah': COUNTRY_PAKISTAN,
                          'PSE': COUNTRY_PHILIPPINES,
                          'SIN': COUNTRY_SINGAPORE,
                          'COL': COUNTRY_SRI_LANKA,
                          'TPE': COUNTRY_TAIWAN,
                          'BAK': COUNTRY_THAILAND,
                          'WBAG': COUNTRY_AUSTRIA,
                          'EBR': COUNTRY_BELGIUM,
                          'BUL': COUNTRY_BULGARIA,
                          'ZSE': COUNTRY_CROATIA,
                          'CSE': COUNTRY_CYPRUS,
                          'PRG': COUNTRY_CZECH_REPUBLIC,
                          'CPH': COUNTRY_DENMARK,
                          'TAL': COUNTRY_ESTONIA,
                          'HEL': COUNTRY_FINLAND,
                          'EPA': COUNTRY_FRANCE,
                          'BER': COUNTRY_GERMANY,
                          'FRA': COUNTRY_GERMANY,
                          'STU': COUNTRY_GERMANY,
                          'ATH': COUNTRY_GREECE,
                          'AMS': COUNTRY_HOLLAND,
                          'BDP': COUNTRY_HUNGARY,
                          'ISE': COUNTRY_IRELAND,
                          'BIT': COUNTRY_ITALTY,
                          'RSE': COUNTRY_LATVIA,
                          'VSE': COUNTRY_LITHUANIA,
                          'LUX': COUNTRY_LUXEMBOURG,
                          'MSE': COUNTRY_MACEDONIA,
                          'OSL': COUNTRY_NORWAY,
                          'WAR': COUNTRY_POLAND,
                          'ELI': COUNTRY_PORTUGAL,
                          'BSE': COUNTRY_ROMANIA,
                          'RTC': COUNTRY_RUSSIA,
                          'LJE': COUNTRY_SLOVENIA,
                          'BCN': COUNTRY_SPAIN,
                          'MCE': COUNTRY_SPAIN,
                          'STO': COUNTRY_SWEDEN,
                          'BRN': COUNTRY_SWITZERLAND,
                          'VTX': COUNTRY_SWITZERLAND,
                          'IST': COUNTRY_TURKEY,
                          'LON': COUNTRY_UK,
                          'OFEX': COUNTRY_UK,
                          'HKG': COUNTRY_HK,
                          'SHA': COUNTRY_CN,
                          'SHE': COUNTRY_CN,
                          'NYSE': COUNTRY_US,
                          'NASDAQ': COUNTRY_US,
                          'AMEX': COUNTRY_US, }

    def __init__(self, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.table = []

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole and role != self.ROLE_SUBTEXT1:
            return QVariant()

        row = self.table[index.row()]
        e = row['e']
        t = row['t']

        if index.column() is self.COL_TICKER:
            str = e + ":" + t
        elif index.column() is self.COL_NAME:
            if role == Qt.DisplayRole:
                n = row['n']
                sugg = row['sugg']
                if len(sugg) > 3:
                    shortName = sugg[2]
                    longName = sugg[3]
                    str = (shortName + " " + longName).decode('utf-8')
                else:
                    str = n.decode('utf-8')
            elif role == self.ROLE_SUBTEXT1:
                country = self.getCountry(e)
                str = '%s (%s)' %(e, country)

        return QVariant(str)

    def getCountry(self, exchange):
        if self.countryExchangeMap.has_key(exchange):
            country = self.countryExchangeMap[exchange]
        else:
            country = self.COUNTRY_UNKNOWN

        return country

    def rowCount(self, parent):
        return len(self.table)

    def columnCount(self, parent):
        return len(self.HEADER)

    def add(self, matches):
        currentRowCount = self.rowCount(self.parent)
        self.beginInsertRows(QModelIndex(), currentRowCount, currentRowCount + len(matches) - 1)
        for match in matches:
            self.table.append(match)
        self.endInsertRows()

    def clear(self):
        self.beginRemoveRows(QModelIndex(), 0, self.rowCount(self.parent) - 1)
        self.table = []
        self.endRemoveRows()

    def reset(self, matches):
        if len(self.table) > 0:
            self.clear()
        self.add(matches)

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.HEADER[col])
        return QVariant()

    def getTicker(self, index):
        row = self.table[index.row()]
        e = row['e']
        t = row['t']
        if t is not None and t is not "":
            if e is not None and e is not "":
                return e + ":" + t
            else:
                return t

        qWarning("Selected entry does not have a valid exchange or ticker.")

