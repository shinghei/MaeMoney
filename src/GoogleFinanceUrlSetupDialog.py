# coding=utf-8

from PyQt4.QtGui import QDialog, QDialogButtonBox, QGridLayout, QLabel, QComboBox, QPushButton
from PyQt4.QtCore import Qt, SIGNAL
from MaeMoneyProperties import MaeMoneyProperties

class GoogleFinanceUrlSetupDialog(QDialog):

    SETTING_GOOGLE_URL = 'googleUrl'
    SETTING_GOOGLE_COUNTRY = 'googleCountry'

    def __init__(self, parent):

        QDialog.__init__(self, parent)

        self.prop = MaeMoneyProperties.instance()
        self.urls = {}
        self.urls[self.prop.GOOGLE_COUNTRY_HK] = 'www.google.com.hk'
        self.urls[self.prop.GOOGLE_COUNTRY_CN] = 'www.google.com.cn'
        self.urls[self.prop.GOOGLE_COUNTRY_CAN] = 'www.google.ca'
        self.urls[self.prop.GOOGLE_COUNTRY_UK] = 'www.google.co.uk'
        self.urls[self.prop.GOOGLE_COUNTRY_US] = 'www.google.com'

        self.setupUi()

    def setupUi(self):
        self.setWindowModality(Qt.WindowModal)
        self.buttonBox = QDialogButtonBox(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.gridLayout = QGridLayout()
        self.setLayout(self.gridLayout)

        self.labelGFinanceUrl = QLabel(self.tr("Google URL"))
        self.gridLayout.addWidget(self.labelGFinanceUrl, 0, 1, 1, 1)
        self.comboBoxGFinanceUrl = QComboBox()
        for [country, url] in sorted(self.urls.iteritems()):
            self.comboBoxGFinanceUrl.addItem(country, url)

        googleCountry = self.prop.getGoogleCountry()
        index = self.comboBoxGFinanceUrl.findText(googleCountry)
        self.comboBoxGFinanceUrl.setCurrentIndex(index)
        self.gridLayout.addWidget(self.comboBoxGFinanceUrl, 0, 2, 1, 1)

        self.gridLayout.addWidget(QLabel(self.tr("Current setting")), 1, 1, 1, 1)
        self.gridLayout.addWidget(QLabel(self.prop.getGoogleCountry()),
                                  1, 2, 1, 1)

        self.setUrlButton = QPushButton(self.tr("Set URL"))
        self.gridLayout.addWidget(self.setUrlButton, 2, 1, 1, 2)

        self.loginErrorMsgLabel = QLabel("")
        self.gridLayout.addWidget(self.loginErrorMsgLabel, 3, 1, 1, 2)

        self.setWindowTitle(self.tr("Setup"))

        self.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
        self.connect(self.setUrlButton, SIGNAL("clicked()"), self.setUrl)

    def setUrl(self):
        indexSelected = self.comboBoxGFinanceUrl.currentIndex()
        country = self.comboBoxGFinanceUrl.itemText(indexSelected)
        url = self.comboBoxGFinanceUrl.itemData(indexSelected).toString().toAscii()
        self.prop.setGoogleCountryUrl(country, url)
        self.accept()
