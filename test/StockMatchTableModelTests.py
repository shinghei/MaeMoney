# coding=gbk

import unittest
from src.StockMatchTableModel import StockMatchTableModel
from PyQt4.QtCore import Qt

class StockMatchTableModelTests(unittest.TestCase):

    def testData(self):
        m = StockMatchTableModel()
        matches = []
        matches.append({'e': 'E', 't': 'T1', 'n': 'N1'})
        matches.append({'e': 'E', 't': 'T2', 'n': 'N2'})
        m.add(matches)
        role = Qt.DisplayRole
        data = m.data(MockQModelIndex(0, 0), role)
        self.assertEquals('E:T1', data)
        data = m.data(MockQModelIndex(0, 1), role)
        self.assertEquals('N1', data)
        data = m.data(MockQModelIndex(1, 0), role)
        self.assertEquals('E:T2', data)
        data = m.data(MockQModelIndex(1, 1), role)
        self.assertEquals('N2', data)

    def testSubText(self):
        m = StockMatchTableModel()
        matches = []
        matches.append({'e': 'HKG', 't': 'T1', 'n': 'N1'})
        matches.append({'e': 'SHE', 't': 'T1', 'n': 'N1'})
        matches.append({'e': 'NYSE', 't': 'T2', 'n': 'N2'})
        matches.append({'e': 'WHAT?', 't': 'T3', 'n': 'N3'})
        m.add(matches)
        role = StockMatchTableModel.ROLE_SUBTEXT1
        data = m.data(MockQModelIndex(0, 1), role)
        self.assertEquals('HKG (香港 Hong Kong)'.decode('chinese'), data)
        data = m.data(MockQModelIndex(1, 1), role)
        self.assertEquals('SHE (中国 China)'.decode('chinese'), data)
        data = m.data(MockQModelIndex(2, 1), role)
        self.assertEquals('NYSE (United States)'.decode('chinese'), data)
        data = m.data(MockQModelIndex(3, 1), role)
        self.assertEquals('WHAT? (Unknown)'.decode('chinese'), data)

    def testColumnCount(self):
        m = StockMatchTableModel()
        self.assertEquals(m.columnCount(None), 2)

    def testRowCount(self):
        m = StockMatchTableModel()
        self.assertEquals(m.rowCount(None), 0)
        matches = []
        matches.append({'e': 'E', 't': 'T1', 'n': 'N1'})
        matches.append({'e': 'E', 't': 'T2', 'n': 'N2'})
        m.add(matches)
        self.assertEquals(m.rowCount(None), 2)
        m.clear()
        self.assertEquals(m.rowCount(None), 0)

    def testReset(self):
        m = StockMatchTableModel()
        matches = []
        matches.append({'e': 'E', 't': 'T1', 'n': 'N1'})
        matches.append({'e': 'E', 't': 'T2', 'n': 'N2'})
        m.add(matches)
        role = Qt.DisplayRole
        data = m.data(MockQModelIndex(0, 0), role)
        self.assertEquals('E:T1', data)
        data = m.data(MockQModelIndex(0, 1), role)
        self.assertEquals('N1', data)
        data = m.data(MockQModelIndex(1, 0), role)
        self.assertEquals('E:T2', data)
        data = m.data(MockQModelIndex(1, 1), role)
        self.assertEquals('N2', data)

        newMatches = []
        newMatches.append({'e': 'E', 't': 'T3', 'n': 'N3'})
        m.reset(newMatches)
        self.assertEquals(1, m.rowCount(None))
        data = m.data(MockQModelIndex(0, 0), role)
        self.assertEquals('E:T3', data)
        data = m.data(MockQModelIndex(0, 1), role)
        self.assertEquals('N3', data)


class MockQModelIndex:

    def __init__(self, row, col):
        self.r = row
        self.c = col

    def isValid(self):
        return True

    def row(self):
        return self.r

    def column(self):
        return self.c