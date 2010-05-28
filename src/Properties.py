# coding=utf-8
from PyQt4.QtCore import QSettings, QString, QLocale

class Properties:

    __instance__ = None

    @staticmethod
    def instance():
        if Properties.__instance__ is None:
            Properties.__instance__ = Properties()

        return Properties.__instance__

    SETTING_GOOGLE_URL = 'google.url'
    SETTING_GOOGLE_COUNTRY = 'google.country'
    GOOGLE_COUNTRY_CN = QString(u'简体中文 (China)')
    GOOGLE_COUNTRY_HK = QString(u'香港版 (Hong Kong)')
    GOOGLE_COUNTRY_CAN = QString(u'Canada')
    GOOGLE_COUNTRY_UK = QString(u'U.K.')
    GOOGLE_COUNTRY_US = QString(u'U.S.')
    GOOGLE_COUNTRY_DEFAULT = GOOGLE_COUNTRY_US

    # See list from http://docs.python.org/library/codecs.html
    ENCODING_BIG5HK = "big5hkscs"
    ENCODING_GBK = "gbk"
    ENCODING_UTF8 = "utf_8"

    def __init__(self):
        self.qSettings = QSettings("cheungs", "Stock Matcher")

        # Map locale to Google country
        self.googleCountries = {}
        self.googleCountries[QLocale.China] = self.GOOGLE_COUNTRY_CN
        self.googleCountries[QLocale.HongKong] = self.GOOGLE_COUNTRY_HK
        self.googleCountries[QLocale.Canada] = self.GOOGLE_COUNTRY_CAN
        self.googleCountries[QLocale.UnitedKingdom] = self.GOOGLE_COUNTRY_UK
        self.googleCountries[QLocale.UnitedStates] = self.GOOGLE_COUNTRY_US

        self.googleUrls = {}
        self.googleUrls[self.GOOGLE_COUNTRY_CN] = 'www.google.com.cn'
        self.googleUrls[self.GOOGLE_COUNTRY_HK] = 'www.google.com.hk'
        self.googleUrls[self.GOOGLE_COUNTRY_CAN] = 'www.google.ca'
        self.googleUrls[self.GOOGLE_COUNTRY_UK] = 'www.google.co.uk'
        self.googleUrls[self.GOOGLE_COUNTRY_US] = 'www.google.com'

        self.encodings = {}
        self.encodings[self.GOOGLE_COUNTRY_CN] = self.ENCODING_GBK
        self.encodings[self.GOOGLE_COUNTRY_HK] = self.ENCODING_BIG5HK
        self.encodings[self.GOOGLE_COUNTRY_CAN] = self.ENCODING_UTF8
        self.encodings[self.GOOGLE_COUNTRY_UK] = self.ENCODING_UTF8
        self.encodings[self.GOOGLE_COUNTRY_US] = self.ENCODING_UTF8

    def clear(self):
        self.qSettings.clear()

    def getGoogleCountry(self, qLocale = None):
        '''
        Precedence: QSettings -> qLocale -> System Locale
        '''
        googleCountry = self.qSettings.value(self.SETTING_GOOGLE_COUNTRY).toString()
        if googleCountry is not None and googleCountry != "":
            return googleCountry

        if qLocale is None:
            qLocale = QLocale.system().country()

        if self.googleCountries.has_key(qLocale):
            googleCountry = self.googleCountries[qLocale]
        else:
            googleCountry = self.GOOGLE_COUNTRY_DEFAULT

        return googleCountry

    def getGoogleUrl(self):
        country = self.getGoogleCountry()

        if self.googleUrls.has_key(country):
            url = self.googleUrls[country]
        else:
            url = self.googleUrls[self.GOOGLE_COUNTRY_DEFAULT]

        return url

    def getEncoding(self):
        country = self.getGoogleCountry()

        if self.encodings.has_key(country):
            enc = self.encodings[country]
        else:
            enc = self.encodings[self.GOOGLE_COUNTRY_DEFAULT]

        return enc

    def setGoogleCountryUrl(self, gCountry, gUrl):
        self.qSettings.setValue(self.SETTING_GOOGLE_URL, QString(gUrl))
        self.qSettings.setValue(self.SETTING_GOOGLE_COUNTRY, QString(gCountry))
