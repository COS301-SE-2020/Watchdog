# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'home_control_panel/app/frontend/gui/HCPMainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(945, 757)
        MainWindow.setMinimumSize(QtCore.QSize(945, 757))
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaContents = QtWidgets.QWidget()
        self.scrollAreaContents.setGeometry(QtCore.QRect(0, 0, 649, 634))
        self.scrollAreaContents.setObjectName("scrollAreaContents")
        self.cameras = QtWidgets.QGridLayout(self.scrollAreaContents)
        self.cameras.setObjectName("cameras")
        self.promptLabel = QtWidgets.QLabel(self.scrollAreaContents)
        self.promptLabel.setObjectName("promptLabel")
        self.cameras.addWidget(self.promptLabel, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaContents)
        self.gridLayout.addWidget(self.scrollArea, 1, 2, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 2, 2, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/images/assets/smallLogo.png"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 3)
        self.locations = QtWidgets.QTreeWidget(self.centralwidget)
        self.locations.setMaximumSize(QtCore.QSize(250, 16777215))
        self.locations.setObjectName("locations")
        self.gridLayout.addWidget(self.locations, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 945, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuCameras = QtWidgets.QMenu(self.menubar)
        self.menuCameras.setObjectName("menuCameras")
        self.menuRecordings = QtWidgets.QMenu(self.menubar)
        self.menuRecordings.setObjectName("menuRecordings")
        self.menuLocations = QtWidgets.QMenu(self.menubar)
        self.menuLocations.setObjectName("menuLocations")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAdd_New_Camera = QtWidgets.QAction(MainWindow)
        self.actionAdd_New_Camera.setObjectName("actionAdd_New_Camera")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAdd_New = QtWidgets.QAction(MainWindow)
        self.actionAdd_New.setObjectName("actionAdd_New")
        self.actionAdd_Webcam = QtWidgets.QAction(MainWindow)
        self.actionAdd_Webcam.setObjectName("actionAdd_Webcam")
        self.actionView_Recordings = QtWidgets.QAction(MainWindow)
        self.actionView_Recordings.setObjectName("actionView_Recordings")
        self.actionAdd_New_Location = QtWidgets.QAction(MainWindow)
        self.actionAdd_New_Location.setObjectName("actionAdd_New_Location")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.menuFile.addAction(self.actionPreferences)
        self.menuFile.addSeparator()
        self.menuCameras.addAction(self.actionAdd_New)
        self.menuCameras.addAction(self.actionAdd_Webcam)
        self.menuRecordings.addAction(self.actionView_Recordings)
        self.menuLocations.addAction(self.actionAdd_New_Location)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuCameras.menuAction())
        self.menubar.addAction(self.menuLocations.menuAction())
        self.menubar.addAction(self.menuRecordings.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Watchdog - Control Panel"))
        self.promptLabel.setText(_translate("MainWindow", "To add a camera go to Cameras > Add New in the Menu above"))
        self.locations.headerItem().setText(0, _translate("MainWindow", "Locations"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuCameras.setTitle(_translate("MainWindow", "Cameras"))
        self.menuRecordings.setTitle(_translate("MainWindow", "Recordings"))
        self.menuLocations.setTitle(_translate("MainWindow", "Locations"))
        self.actionAdd_New_Camera.setText(_translate("MainWindow", "Add New Camera"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAdd_New.setText(_translate("MainWindow", "Add New"))
        self.actionAdd_Webcam.setText(_translate("MainWindow", "Add Webcam"))
        self.actionView_Recordings.setText(_translate("MainWindow", "View Recordings"))
        self.actionAdd_New_Location.setText(_translate("MainWindow", "Add New Location"))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences"))

from . import resources_rc
