# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'home_control_panel/app/frontend/gui/SettingsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.setWindowModality(QtCore.Qt.ApplicationModal)
        Settings.resize(796, 603)
        Settings.setMinimumSize(QtCore.QSize(796, 603))
        Settings.setModal(True)
        self.gridLayout_3 = QtWidgets.QGridLayout(Settings)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.updateSettings = QtWidgets.QPushButton(Settings)
        self.updateSettings.setObjectName("updateSettings")
        self.gridLayout_3.addWidget(self.updateSettings, 2, 1, 1, 1)
        self.statusBar = QtWidgets.QLabel(Settings)
        self.statusBar.setText("")
        self.statusBar.setObjectName("statusBar")
        self.gridLayout_3.addWidget(self.statusBar, 3, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Settings)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setObjectName("formLayout")
        self.site = QtWidgets.QLineEdit(self.groupBox)
        self.site.setObjectName("site")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.site)
        self.address = QtWidgets.QTextEdit(self.groupBox)
        self.address.setObjectName("address")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.address)
        self.live = QtWidgets.QComboBox(self.groupBox)
        self.live.setObjectName("live")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.live)
        self.recordingRatio = QtWidgets.QDial(self.groupBox)
        self.recordingRatio.setWrapping(False)
        self.recordingRatio.setNotchesVisible(True)
        self.recordingRatio.setObjectName("recordingRatio")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.recordingRatio)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label)
        self.recordingRatioValue = QtWidgets.QLabel(self.groupBox)
        self.recordingRatioValue.setObjectName("recordingRatioValue")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.recordingRatioValue)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 4, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Settings)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox_4)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 2, 3, 3, 1)
        self.width = QtWidgets.QSlider(self.groupBox_4)
        self.width.setMinimum(240)
        self.width.setMaximum(720)
        self.width.setSingleStep(10)
        self.width.setProperty("value", 360)
        self.width.setOrientation(QtCore.Qt.Horizontal)
        self.width.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.width.setObjectName("width")
        self.gridLayout.addWidget(self.width, 1, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_4)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1)
        self.height = QtWidgets.QSlider(self.groupBox_4)
        self.height.setMinimum(100)
        self.height.setMaximum(500)
        self.height.setSingleStep(10)
        self.height.setOrientation(QtCore.Qt.Vertical)
        self.height.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.height.setObjectName("height")
        self.gridLayout.addWidget(self.height, 3, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_4)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 1, 1, 1)
        self.widthValue = QtWidgets.QLabel(self.groupBox_4)
        self.widthValue.setObjectName("widthValue")
        self.gridLayout.addWidget(self.widthValue, 0, 1, 1, 1)
        self.heightValue = QtWidgets.QLabel(self.groupBox_4)
        self.heightValue.setObjectName("heightValue")
        self.gridLayout.addWidget(self.heightValue, 1, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox_4)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_4, 1, 0, 1, 1)
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox_5)
        self.formLayout_2.setObjectName("formLayout_2")
        self.clipLength = QtWidgets.QDial(self.groupBox_5)
        self.clipLength.setNotchesVisible(True)
        self.clipLength.setObjectName("clipLength")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.clipLength)
        self.framesPerSecond = QtWidgets.QDial(self.groupBox_5)
        self.framesPerSecond.setMinimum(1)
        self.framesPerSecond.setMaximum(60)
        self.framesPerSecond.setProperty("value", 2)
        self.framesPerSecond.setNotchTarget(1.0)
        self.framesPerSecond.setNotchesVisible(True)
        self.framesPerSecond.setObjectName("framesPerSecond")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.framesPerSecond)
        self.label_3 = QtWidgets.QLabel(self.groupBox_5)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.clipLengthValue = QtWidgets.QLabel(self.groupBox_5)
        self.clipLengthValue.setObjectName("clipLengthValue")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.clipLengthValue)
        self.framesPerSecondValue = QtWidgets.QLabel(self.groupBox_5)
        self.framesPerSecondValue.setObjectName("framesPerSecondValue")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.framesPerSecondValue)
        self.label_2 = QtWidgets.QLabel(self.groupBox_5)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.gridLayout_2.addWidget(self.groupBox_5, 2, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(Settings)
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", -1)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_3.addWidget(self.progressBar, 1, 1, 1, 1)

        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Settings"))
        self.updateSettings.setText(_translate("Settings", "Update"))
        self.groupBox.setTitle(_translate("Settings", "Basic "))
        self.label_6.setText(_translate("Settings", "Site Name"))
        self.label_7.setText(_translate("Settings", "Address"))
        self.label_8.setText(_translate("Settings", "Live"))
        self.label.setText(_translate("Settings", "Recordings Ratio"))
        self.recordingRatioValue.setText(_translate("Settings", "Value"))
        self.groupBox_2.setTitle(_translate("Settings", "Video Recordings"))
        self.textBrowser.setHtml(_translate("Settings", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Video Resolution</p></body></html>"))
        self.label_4.setText(_translate("Settings", "Width"))
        self.label_5.setText(_translate("Settings", "Height"))
        self.widthValue.setText(_translate("Settings", "width"))
        self.heightValue.setText(_translate("Settings", "height"))
        self.label_11.setText(_translate("Settings", "x"))
        self.label_3.setText(_translate("Settings", "Frames per Second"))
        self.clipLengthValue.setText(_translate("Settings", "Value"))
        self.framesPerSecondValue.setText(_translate("Settings", "Value"))
        self.label_2.setText(_translate("Settings", "Clip Length"))