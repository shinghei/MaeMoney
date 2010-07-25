# coding=big5

import unittest
import src.Util
from src.Util import *
from src.StockMatchGoogleFinance import *

class UtilTests(unittest.TestCase):

    def testEncoding(self):
        original = u"Hello / World 你"
        unicodeEncoded = unicode.encode(original, "big5")
        print "unicodeEncoded: " + unicodeEncoded
        unicodeEscaped = original.encode('big5')
        print "unicodeEscaped: " + unicodeEscaped

        str = "Hello \x2f World"
        self.assertEquals("Hello / World", str)

    def testReplace(self):
        str = "Hello \\x2f World"
        s = Util.evalJson(str)
        self.assertEquals("Hello / World", s)

    def testCode(self):
        a = {"matches" : [{"t":"MCD", "n":"McDonald\x27s Corporation", "e":"NYSE", "id":"22568", "sugg":["1,2","MCD","McDonald\'s Corporation"]}],"all":True}
        matches = a['matches']
        self.assertTrue(matches is not None)
        str = '{\"matches\" : [{\"t\":\"MCD\", \"n\":\"McDonald\\x27s Corporation\", \"e\":\"NYSE\", \"id\":\"22568\", \"sugg\":[\"1,2\",\"MCD\",\"McDonald\'s Corporation\"]}],\"all\":True}'
        a = eval(str)
        print a

    def testTrueFalseCasing(self):
        trueFalse = "Blah Blah:true true Blah:false false Blah"
        replaced = Util.convertTrueFalseCasing(trueFalse)
        self.assertEquals("Blah Blah:True True Blah:False False Blah", replaced)

    def testConvertToJson(self):
        f = open('matches-0005.txt', 'r')
        s = f.read()

        gf = StockMatchGoogleFinance()
        cleaned = gf.cleanUpDataFromGoogle(s)
        json = gf.convertToJson(cleaned)
        self.assertTrue(json['matches'] is not None)

    def testMatcher(self):
        gf = StockMatchGoogleFinance()
        matches = gf.match("HKG:0005")
        self.assertEquals(1, len(matches))
        sugg = matches[0]['sugg']
        self.assertEquals("0005", sugg[1])

    def testLoadJsonString(self):
        f = open('quotes.txt', 'r')
        s = f.read()

        decoded = Util.loadsJsonString(s, 'big5')
        print decoded

    def testExtractDate(self):
        dateStr = '2010-07-08T123234235'
        extracted = Util.extractDate(dateStr)

        self.assertEquals('2010-07-08', extracted)

        dateStr = '2010-07-xxT12341234'
        extracted = Util.extractDate(dateStr)
        self.assertEquals(None, extracted)
