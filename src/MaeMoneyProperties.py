# coding=utf-8
from Properties import Properties

class MaeMoneyProperties:

    __instance__ = None

    @staticmethod
    def instance():
        '''
        @param application string
        '''
        if MaeMoneyProperties.__instance__ is None:
            MaeMoneyProperties.__instance__ = Properties("MaeMoney")

        return MaeMoneyProperties.__instance__