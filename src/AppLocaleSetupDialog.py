# coding=utf-8

from PyQt4.QtGui import QDialog, QDialogButtonBox, QGridLayout, QLabel, QComboBox, QPushButton
from PyQt4.QtCore import Qt, SIGNAL
from MaeMoneyProperties import MaeMoneyProperties

class AppLocaleSetupDialog(QDialog):

    def __init__(self, parent):

        QDialog.__init__(self, parent)

        self.prop = MaeMoneyProperties.instance()
        self.locales = {}
        self.locales[self.prop.LANGUAGE_ZH_HK] = self.prop.LOCALE_ZH_HK
        self.locales[self.prop.LANGUAGE_EN_US] = self.prop.LOCALE_EN_US

        self.setupUi()

    def setupUi(self):
        self.setWindowModality(Qt.WindowModal)
        self.buttonBox = QDialogButtonBox(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.gridLayout = QGridLayout()
        self.setLayout(self.gridLayout)

        self.labelAppLocale = QLabel(u"語言 Language")
        self.gridLayout.addWidget(self.labelAppLocale, 0, 1, 1, 1)
        self.comboBoxAppLocale = QComboBox()
        for [lang, appLocale] in sorted(self.locales.iteritems()):
            self.comboBoxAppLocale.addItem(lang, appLocale)

        language = self.prop.getAppLanguage()
        index = self.comboBoxAppLocale.findText(language)
        self.comboBoxAppLocale.setCurrentIndex(index)
        self.gridLayout.addWidget(self.comboBoxAppLocale, 0, 2, 1, 1)

        self.gridLayout.addWidget(QLabel(self.tr("Current setting")), 1, 1, 1, 1)
        self.gridLayout.addWidget(QLabel(self.prop.getAppLanguage()),
                                  1, 2, 1, 1)

        self.setLanguageButton = QPushButton(self.tr("Set language"))
        self.gridLayout.addWidget(self.setLanguageButton, 2, 1, 1, 2)

        self.setWindowTitle(self.tr("Language setup"))

        self.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
        self.connect(self.setLanguageButton, SIGNAL("clicked()"), self.setLanguage)

    def setLanguage(self):
        indexSelected = self.comboBoxAppLocale.currentIndex()
        locale = self.comboBoxAppLocale.itemData(indexSelected)
        self.prop.setAppLocale(locale)
        self.accept()

#        try:
#            from PyQt4.QtMaemo5 import QMaemo5InformationBox
#            timeoutInMs = 3000
#            QMaemo5InformationBox.information(
#                    self.parent,
#                    self.tr("Language change will take effect next time when you run Stock Matcher"),
#                    timeoutInMs)
#        except ImportError:
#            qDebug("Can't use QMaemo5InformationBox")

