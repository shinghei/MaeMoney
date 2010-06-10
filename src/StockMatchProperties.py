# coding=utf-8
from Properties import Properties

class StockMatchProperties:

    __instance__ = None

    @staticmethod
    def instance():
        '''
        @param application string
        '''
        if StockMatchProperties.__instance__ is None:
            StockMatchProperties.__instance__ = Properties("Stock Matcher")

        return StockMatchProperties.__instance__