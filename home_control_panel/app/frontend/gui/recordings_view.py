# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'home_control_panel/app/frontend/gui/RecordingsView.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RecordingsView(object):
    def setupUi(self, RecordingsView):
        RecordingsView.setObjectName("RecordingsView")
        RecordingsView.setWindowModality(QtCore.Qt.ApplicationModal)
        RecordingsView.resize(579, 417)
        RecordingsView.setMinimumSize(QtCore.QSize(579, 367))
        RecordingsView.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(RecordingsView)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.exit = QtWidgets.QPushButton(RecordingsView)
        self.exit.setObjectName("exit")
        self.horizontalLayout_2.addWidget(self.exit)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.directory = QtWidgets.QTreeView(RecordingsView)
        self.directory.setObjectName("directory")
        self.gridLayout.addWidget(self.directory, 0, 0, 1, 1)

        self.retranslateUi(RecordingsView)
        QtCore.QMetaObject.connectSlotsByName(RecordingsView)

    def retranslateUi(self, RecordingsView):
        _translate = QtCore.QCoreApplication.translate
        RecordingsView.setWindowTitle(_translate("RecordingsView", "Recordings"))
        self.exit.setText(_translate("RecordingsView", "Exit"))
