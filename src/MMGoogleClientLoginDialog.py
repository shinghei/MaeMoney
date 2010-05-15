from PyQt4 import Qt, QtCore, QtGui
from PyQt4.Qt import *
from PyQt4.QtGui import *
from gdata.finance.service import *
from gdata.service import BadAuthentication, CaptchaRequired
import base64

class MMGoogleClientLoginDialog(QDialog):

    def __init__(self, parent, controller):

        QDialog.__init__(self, parent)
        self.setupUi()
        self.controller = controller

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
        self.setWindowModality(Qt.WindowModal)
        self.buttonBox = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.gridLayout = QtGui.QGridLayout()
        self.setLayout(self.gridLayout)

        self.userNameLabel = QLabel("User name")
        self.gridLayout.addWidget(self.userNameLabel, 0, 1, 1, 1)
        self.userNameLineEdit = QLineEdit()
        self.gridLayout.addWidget(self.userNameLineEdit, 0, 2, 1, 1)

        self.passwordLabel = QLabel("Password")
        self.gridLayout.addWidget(self.passwordLabel, 1, 1, 1, 1)
        self.passwordLineEdit = QtGui.QLineEdit()
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.gridLayout.addWidget(self.passwordLineEdit, 1, 2, 1, 1)

        self.loginButton = QtGui.QPushButton("Login")
        self.gridLayout.addWidget(self.loginButton, 2, 1, 1, 2)

        self.loginErrorMsgLabel = QtGui.QLabel("")
        self.gridLayout.addWidget(self.loginErrorMsgLabel, 3, 1, 1, 2)

        self.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
        self.connect(self.loginButton, SIGNAL("clicked()"), self.credentialsEntered)
        self.connect(self.passwordLineEdit, SIGNAL("returnPressed()"), self.loginButton.click)

    def credentialsEntered(self):
        userName = self.userNameLineEdit.text().toAscii()
        password = self.passwordLineEdit.text().toAscii()
        try:
            self.controller.login(userName, password)
            self.loginErrorMsgLabel.clear()
            self.accept()
            self.settings.setValue("username", userName)
            self.settings.setValue("password", base64.encodestring(password))
        except BadAuthentication:
            self.passwordLineEdit.clear()
            self.passwordLineEdit.setFocus()
            self.loginErrorMsgLabel.setText("BadAuthentication: Wrong username or password.")
        except CaptchaRequired:
            self.passwordLineEdit.clear()
            self.userNameLineEdit.setFocus()
            self.loginErrorMsgLabel.setText("CaptchaRequired: Wrong username or password.")
