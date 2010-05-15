import unittest
from src.RealtimeQuoter import *
from sets import Set

class RealtimeQuoterTests(unittest.TestCase):

    def testSortByExchange(self):
        tickers = [["NYSE", "HBC"], ["NYSE", "GE"], ["NYSE", "GE"], ["HKG", "0005"]]
        updateThread = UpdateThread("TestThread", None, tickers)
        grouped = updateThread.groupTickersByExchange(tickers)
        self.assertEquals(2, len(grouped))
        self.assertEquals(["HBC", "GE", "GE"], grouped["NYSE"])
        self.assertEquals(["0005"], grouped["HKG"])

    def testCountryMergeExchangeTicker(self):
        country = Country("", "")
        tickers = ["GE", "HBC", "GOOG"]
        merged = country.mergeExchangeTickers("NYSE", tickers)
        self.assertEquals("NYSE:GE,NYSE:HBC,NYSE:GOOG", merged)
        # Ensure the original tickers list is not changed in the course of merging with the exchange
        self.assertEquals(["GE", "HBC", "GOOG"], tickers)

    def testGetRealTimeQuotes(self):
        country = Country('big5', 'www.google.com')
        country.getRealTimeQuotes('NYSE', ['MCD'])