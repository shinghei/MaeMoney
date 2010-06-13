# -*- coding: utf-8 -*-

import unittest
from src.Properties import *
from PyQt4.QtCore import QLocale

class PropertiesTests(unittest.TestCase):

    def testGetGoogleCountry(self):
        prop = Properties.instance()

        # Clear all existing QSettings
        prop.clear()

        uk = prop.getGoogleCountry(QLocale.UnitedKingdom)
        self.assertEquals(u"U.K.", uk)

        us = prop.getGoogleCountry(QLocale.UnitedStates)
        self.assertEquals(u"U.S.", us)

        cn = prop.getGoogleCountry(QLocale.China)
        self.assertEquals(QString(u'简体中文 (China)'), cn)

        hk = prop.getGoogleCountry(QLocale.HongKong)
        self.assertEquals(QString(u'香港版 (Hong Kong)'), hk)

        hk = prop.getGoogleCountry()
        self.assertEquals(QString(u'香港版 (Hong Kong)'), hk)

        prop.setGoogleCountryUrl(u"U.K.", u"www.google.co.uk")
        country = prop.getGoogleCountry()
        self.assertEquals(u"U.K.", country)

        # Test the fallback country
        prop.clear()
        country = prop.getGoogleCountry(QLocale.AnyCountry)
        self.assertEquals(u"U.S.", country)

    def testGetGoogleUrl(self):

        prop = Properties.instance()
        prop.clear()

        url = prop.getGoogleUrl()
        self.assertEquals("www.google.com.hk", url)

        prop.setGoogleCountryUrl(u"U.K.", "www.google.co.uk")
        url = prop.getGoogleUrl()
        self.assertEquals("www.google.co.uk", url)

        prop.setGoogleCountryUrl(u"Unknown", "what.ever")
        url = prop.getGoogleUrl()
        self.assertEquals("www.google.com", url)

    def testGetEncoding(self):

        prop = Properties.instance()
        prop.clear()

        enc = prop.getEncoding()
        self.assertEquals(Properties.ENCODING_BIG5HK, enc)

        prop.setGoogleCountryUrl(QString(u'简体中文 (China)'), "www.google.com.cn")
        enc = prop.getEncoding()
        self.assertEquals(Properties.ENCODING_GBK, enc)

        prop.setGoogleCountryUrl(QString(u'香港版 (Hong Kong)'), "www.google.com.hk")
        enc = prop.getEncoding()
        self.assertEquals(Properties.ENCODING_BIG5HK, enc)

        prop.setGoogleCountryUrl(u"U.K.", "www.google.co.uk")
        enc = prop.getEncoding()
        self.assertEquals(Properties.ENCODING_UTF8, enc)

        prop.setGoogleCountryUrl(u"Unknown", "what.ever")
        enc = prop.getEncoding()
        self.assertEquals(Properties.ENCODING_UTF8, enc)

    def testMultipleInstances(self):
        prop1 = Properties.instance()
        prop2 = Properties.instance()

        self.assertEquals(prop1, prop2)

    def testAppLocale(self):
        prop = Properties.instance()
        prop.clear()
        l = prop.getAppLocale()
        self.assertEquals(QLocale.HongKong, l.country())
        self.assertEquals(QLocale.Chinese, l.language())

        locale = QLocale.Bangladesh
        prop.setAppLocale(locale)

        l = prop.getAppLocale()

        self.assertEquals(locale, l)

    def testLocales(self):
        zh_hk = QLocale(QLocale.Chinese, QLocale.HongKong)
        en_us = QLocale(QLocale.English, QLocale.UnitedStates)

        self.assertEquals(QLocale.Chinese, zh_hk.language())
        self.assertEquals(QLocale.HongKong, zh_hk.country())

        self.assertEquals(QLocale.English, en_us.language())
        self.assertEquals(QLocale.UnitedStates, en_us.country())

        appLangs = {}
        appLangs[zh_hk] = "zh_hk"
        self.assertEquals(appLangs[zh_hk], "zh_hk")
