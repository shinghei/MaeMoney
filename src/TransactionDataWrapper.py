from Util import Util

class TransactionDataWrapper:

    def __init__(self, transactionData):
        '''
        @param transactionData - Type: gdata.finance.TransactionEntry
        '''
        self.tData = transactionData

    def getType(self):
        '''
        Type of transaction - Buy or Sell
        @returns string
        '''
        return self.tData.type

    def getDate(self):
        '''
        @returns string
        '''
        date = Util.extractDate(self.tData.date)
        return date

    def getShares(self):
        '''
        @returns float - Number of shares involved in this transaction
        '''
        return self.strToFloat(self.tData.shares)

    def getUnitPrice(self):
        '''
        @returns float - unit price
        '''
        return self.strToFloat(self.tData.price.money[0].amount)

    def getCommission(self):
        '''
        @returns float - Commission tendered
        '''
        return self.strToFloat(self.tData.commission.money[0].amount)

    def getCurrency(self):
        '''
        @returns string - Currency of commission tendered
        '''
        return self.tData.commission.money[0].currency_code


    def strToFloat(self, s):
        try:
            return float(s)
        except ValueError:
            return None