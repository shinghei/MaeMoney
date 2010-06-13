from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QSettings, SIGNAL
from PyQt4.QtGui import QDialog, QDialogButtonBox, QLabel, QLineEdit, QPushButton
import base64
import string

class MMGoogleClientLoginDialog(QDialog):

    def __init__(self, parent):

        QDialog.__init__(self, parent)
        self.setupUi()

        self.userNameLineEdit.setFocus()

        self.settings = QSettings("cheungs", "MaeMoney")
        settingUsername = self.settings.value("username")
        settingPassword = self.settings.value("password")
        if settingUsername is not "":
            self.userNameLineEdit.setText(settingUsername.toString())
            self.passwordLineEdit.setFocus()
        if settingPassword is not "":
            self.passwordLineEdit.setText(base64.decodestring(settingPassword.toString()))
            self.loginButton.setFocus()

    def setupUi(self):
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.buttonBox = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.gridLayout = QtGui.QGridLayout()
        self.setLayout(self.gridLayout)

        self.userNameLabel = QLabel(self.tr("User name"))
        self.gridLayout.addWidget(self.userNameLabel, 0, 1, 1, 1)
        self.userNameLineEdit = QLineEdit()
        self.gridLayout.addWidget(self.userNameLineEdit, 0, 2, 1, 1)

        self.passwordLabel = QLabel(self.tr("Password"))
        self.gridLayout.addWidget(self.passwordLabel, 1, 1, 1, 1)
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.gridLayout.addWidget(self.passwordLineEdit, 1, 2, 1, 1)

        self.loginButton = QPushButton(self.tr("Login"))
        self.gridLayout.addWidget(self.loginButton, 2, 1, 1, 2)

        self.loginErrorMsgLabel = QLabel("")
        self.gridLayout.addWidget(self.loginErrorMsgLabel, 3, 1, 1, 2)

        self.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
        self.connect(self.loginButton, SIGNAL("clicked()"), self.credentialsEntered)
        self.connect(self.passwordLineEdit, SIGNAL("returnPressed()"), self.loginButton.click)

    def credentialsEntered(self):
        userName = self.userNameLineEdit.text().toAscii()
        password = self.passwordLineEdit.text().toAscii()
        self.emit(SIGNAL("credentialsEntered(string, string)"), userName, password)

    def acceptCredentials(self, userName, password):
        self.loginErrorMsgLabel.clear()
        self.accept()
        self.settings.setValue("username", userName)
        self.settings.setValue("password", base64.encodestring(password))

    def rejectCredentials(self, reason):
        self.passwordLineEdit.clear()
        self.passwordLineEdit.setFocus()
        self.loginErrorMsgLabel.setText(reason)

