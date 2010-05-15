# coding=big5

import unittest
import urllib

from PyQt4.Qt import QString

class StockMatchTests(unittest.TestCase):

    def testUrlEncode(self):

        qs = QString("Hello World")
        s = str(qs)
        quoted = urllib.quote(str(s))
        self.assertEquals("Hello%20World", quoted)

        qs = QString(unicode("你 好", 'big5'))
        u = unicode(qs.toUtf8(),'utf8').encode('utf8')
        s = str(u)
        quoted = urllib.quote(str(s))
        self.assertEquals('%E4%BD%A0%20%E5%A5%BD', quoted)

