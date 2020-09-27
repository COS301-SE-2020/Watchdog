from PyQt5 import QtWidgets
import sys
import time

from home_control_panel.app.frontend.Interface import Interface
from home_control_panel.app.frontend.gui.add_camera_dialog import Ui_AddCamera
from home_control_panel.app.frontend.gui.login_dialog import Ui_Login
from home_control_panel.app.frontend.gui.main_window import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Interface):
    def __init__(self, controller_events: dict):
        super().__init__(controller_events=controller_events)
        self.loggedIn = False

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Login Dialog
        self.login_dialog = QtWidgets.QDialog()
        self.login_dialog.ui = Ui_Login()
        self.login_dialog.ui.setupUi(self.login_dialog)
        self.login_dialog.ui.progressBar.hide()
        self.login_dialog.ui.login.clicked.connect(self.login_event)

        # Add Camera Dialog
        self.add_camera_dialog = QtWidgets.QDialog()
        self.add_camera_dialog.ui = Ui_AddCamera()
        self.add_camera_dialog.ui.setupUi(self.add_camera_dialog)
        self.add_camera_dialog.ui.progressBar.hide()

        # Connect UI events to controller_events
        self.ui.actionAdd_New.triggered.connect(self.trigger_add_camera)

    def trigger_add_camera(self, callback=None):
        self.add_camera_dialog.exec_()
        log("CAMERA")
        pass

    def login_event(self):
        self.login_dialog.ui.progressBar.show()
        username = self.login_dialog.ui.usernameInput.text()
        password = self.login_dialog.ui.passwordInput.text()

        self.login_dialog.ui.usernameInput.setDisabled(True)
        self.login_dialog.ui.passwordInput.setDisabled(True)

        fine = True

        if username == '':
            fine = False
            self.login_dialog.ui.usernameInput.setStyleSheet('border: 1px solid red;')

        if password == '':
            fine = False
            self.login_dialog.ui.passwordInput.setStyleSheet('border: 1px solid red;')

        if fine:
            self.loggedIn = self.controller_events["login"](username, password)

            # If logged in exit login dialog
            if self.loggedIn:
                self.login_dialog.close()
            else:
                self.login_dialog.ui.statusBar.setText('Login Failed. Please Check Credentials...')

        self.login_dialog.ui.usernameInput.setDisabled(False)
        self.login_dialog.ui.passwordInput.setDisabled(False)
        self.login_dialog.ui.progressBar.hide()

    def login(self, callback=None):
        self.hide()
        self.login_dialog.exec_()

        if self.loggedIn:
            self.show()
        else:
            self.close()
            sys.exit(0)


def log(obj=None):
    print(obj)


app = QtWidgets.QApplication([])
app.setStyle('Fusion')


def temp_login(username, password):
    print(f'Controller: Logging in {{username: {username}, password: {password}}}'),
    return username == "Rishi" and password == "Test@123"


application = MainWindow(
    controller_events={
        "start": lambda x: print("Controller: Starting..."),
        "stop": lambda x: print("Controller: Stopping..."),
        "login": temp_login,
        "logout": lambda x: print("Controller: Logging out..."),
        "add_camera": lambda protocol, ip, path, name, location: print(f'Controller: Adding Camera - {name}: {{'
                                                                       f'protocol: {protocol}, ip: {ip}, '
                                                                       f'path: {path}, location: {location}}}'),
        "remove_camera": lambda id: print(f'Controller: Removing Camera - id: {id}'),
        "add_location": lambda name: print(f'Controller: Adding Location - name: {name}'),
        "remove_location": lambda id: print(f'Controller: Removing Location - id: {id}')
    }
)

# application.show()
application.login(log)
sys.exit(app.exec_())
