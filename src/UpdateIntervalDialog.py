# coding=utf-8

from PyQt4.QtGui import QDialog, QDialogButtonBox, QGridLayout, QLabel, QComboBox, QPushButton, QVBoxLayout
from PyQt4.QtCore import Qt, SIGNAL, qWarning
from MaeMoneyProperties import MaeMoneyProperties
from Properties import Properties

class UpdateIntervalDialog(QDialog):

    def __init__(self, parent, updater):

        QDialog.__init__(self, parent)

        self.updater = updater
        self.prop = MaeMoneyProperties.instance()
        self.setupUi()

    def setupUi(self):
        self.setWindowModality(Qt.WindowModal)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.btnPauseUpdate = QPushButton()
        self.setPauseUpdateButtonStatus()
        self.layout.addWidget(self.btnPauseUpdate)

        self.comboBoxUpdInterval = QComboBox()
        self.comboBoxUpdInterval.addItem(self.tr("Pause update"), 0)
        self.comboBoxUpdInterval.addItem(
                self.tr("Update interval - %1s").arg(Properties.DEFAULT_UPDATE_INTERVAL),
                Properties.DEFAULT_UPDATE_INTERVAL)
        self.comboBoxUpdInterval.addItem(self.tr("Update interval - 25s"), 25)
        self.comboBoxUpdInterval.addItem(self.tr("Update interval - 1 min"), 60)
        self.comboBoxUpdInterval.addItem(self.tr("Update interval - 5 min"), 5 * 60)
        self.comboBoxUpdInterval.addItem(self.tr("Update interval - 15 min"), 15 * 60)
        self.comboBoxUpdInterval.addItem(self.tr("Update interval - 30 min"), 30 * 60)
        self.comboBoxUpdInterval.addItem(self.tr("Update interval - 45 min"), 45 * 60)
        self.comboBoxUpdInterval.addItem(self.tr("Update interval - 1 hr"), 1 * 60 * 60)
        self.comboBoxUpdInterval.addItem(self.tr("Update interval - 2 hr"), 2 * 60 * 60)
        self.setCurrentComboBoxUpdInterval()
        self.setComboBoxStatus()
        self.layout.addWidget(self.comboBoxUpdInterval)

        self.btnBackToMainApp = QPushButton(self.tr("Back to Main Application"))
        self.layout.addWidget(self.btnBackToMainApp)

        self.setWindowTitle(self.tr("Update Interval"))

        self.connect(self.btnPauseUpdate, SIGNAL("clicked()"), self.pauseUpdate)
        self.connect(self.comboBoxUpdInterval, SIGNAL("activated(int)"), self.updateIntervalSelected)
        self.connect(self.btnBackToMainApp, SIGNAL("clicked()"), self.accept)

    def setCurrentComboBoxUpdInterval(self):
        curInterval = self.prop.getUpdateInterval()
        index = self.comboBoxUpdInterval.findData(curInterval)
        if index >= 0:
            self.comboBoxUpdInterval.setCurrentIndex(index)
        else:
            qWarning("Update interval of %ds is not available." %(curInterval))
            qWarning("Resetting to default of %ds" %(Properties.DEFAULT_UPDATE_INTERVAL))
            self.prop.setUpdateInterval(Properties.DEFAULT_UPDATE_INTERVAL)
            self.setCurrentComboBoxUpdInterval()

    def updateIntervalSelected(self, index):
        if self.updater is not None:
            intervalSelected = self.comboBoxUpdInterval.itemData(index).toInt()[0]
            self.prop.setUpdateInterval(intervalSelected)
            if intervalSelected == 0:
                self.pauseUpdate()
            else:
                self.updater.terminate()
                self.updater.start()
                self.updater.setUpdateInterval(intervalSelected)
                self.setPauseUpdateButtonStatus()

    def pauseUpdate(self):
        if self.updater is not None:
            self.updater.terminate()
            self.setPauseUpdateButtonStatus()
            pauseInterval = 0
            index = self.comboBoxUpdInterval.findData(pauseInterval)
            self.comboBoxUpdInterval.setCurrentIndex(index)
            self.prop.setUpdateInterval(pauseInterval)

    def setPauseUpdateButtonStatus(self):
        if self.btnPauseUpdate is not None:
            if self.updater is not None and self.updater.isRunning():
                self.btnPauseUpdate.setText(self.tr("Timer currently active. Click to pause update"))
                self.btnPauseUpdate.setEnabled(True)
            else:
                self.btnPauseUpdate.setText(self.tr("Update not running"))
                self.btnPauseUpdate.setEnabled(False)

    def setComboBoxStatus(self):
        if self.comboBoxUpdInterval is not None:
            if self.updater is None:
                self.comboBoxUpdInterval.setEnabled(False)
            else:
                self.comboBoxUpdInterval.setEnabled(True)