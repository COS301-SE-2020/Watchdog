# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/LoginDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(383, 300)
        Login.setMinimumSize(QtCore.QSize(383, 193))
        Login.setMaximumSize(QtCore.QSize(400, 300))
        self.gridLayout = QtWidgets.QGridLayout(Login)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(Login)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setObjectName("formLayout")
        self.usernameInput = QtWidgets.QLineEdit(self.groupBox)
        self.usernameInput.setObjectName("usernameInput")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.usernameInput)
        self.passwordInput = QtWidgets.QLineEdit(self.groupBox)
        self.passwordInput.setInputMask("")
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordInput.setObjectName("passwordInput")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.passwordInput)
        self.login = QtWidgets.QPushButton(self.groupBox)
        self.login.setObjectName("login")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.login)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)
        self.WatchdogLogo = QtWidgets.QLabel(Login)
        self.WatchdogLogo.setObjectName("WatchdogLogo")
        self.gridLayout.addWidget(self.WatchdogLogo, 0, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(Login)
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", -1)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 2, 0, 1, 1)

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Dialog"))
        self.login.setText(_translate("Login", "Login"))
        self.label.setText(_translate("Login", "Username"))
        self.label_2.setText(_translate("Login", "Password"))
        self.WatchdogLogo.setText(_translate("Login", "Watchdog Control Panel"))