from PyQt5 import QtWidgets
import sys

from PyQt5.QtWidgets import QTreeWidgetItem

from home_control_panel.app.frontend.Interface import Interface
from home_control_panel.app.frontend.gui.add_camera_dialog import Ui_AddCamera
from home_control_panel.app.frontend.gui.add_location_dialog import Ui_AddLocation
from home_control_panel.app.frontend.gui.login_dialog import Ui_Login
from home_control_panel.app.frontend.gui.main_window import Ui_MainWindow
from home_control_panel.app.frontend.gui.recordings_view import Ui_RecordingsView
from home_control_panel.app.frontend.gui.repair_camera_dialog import Ui_RepairCamera
from home_control_panel.app.frontend.gui.stream_view import Ui_StreamView


class ControlPanel(QtWidgets.QMainWindow, Interface):
    def __init__(self, controller_events: dict):
        super().__init__(controller_events=controller_events)
        self.loggedIn = False
        self.camera_elements_row = 0
        self.camera_elements_column = 0

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.progressBar.hide()

        # Login Dialog
        self.login_dialog = QtWidgets.QDialog()
        self.login_dialog.ui = Ui_Login()
        self.login_dialog.ui.setupUi(self.login_dialog)
        self.login_dialog.ui.progressBar.hide()
        self.login_dialog.ui.login.clicked.connect(self.__login_event)

        # Repair Camera Dialog
        self.repair_camera_dialog = QtWidgets.QDialog()
        self.repair_camera_dialog.ui = Ui_RepairCamera()
        self.repair_camera_dialog.ui.setupUi(self.repair_camera_dialog)
        self.repair_camera_dialog.ui.progressBar.hide()
        self.repair_camera_dialog.ui.fixCamera.clicked.connect(self.__repair_camera_event)

        # Add Camera Dialog
        self.add_camera_dialog = QtWidgets.QDialog()
        self.add_camera_dialog.ui = Ui_AddCamera()
        self.add_camera_dialog.ui.setupUi(self.add_camera_dialog)
        self.add_camera_dialog.ui.progressBar.hide()
        self.add_camera_dialog.ui.addCamera.clicked.connect(self.__add_camera_event)

        # Add Locations Dialog
        self.add_location_dialog = QtWidgets.QDialog()
        self.add_location_dialog.ui = Ui_AddLocation()
        self.add_location_dialog.ui.setupUi(self.add_location_dialog)
        self.add_location_dialog.ui.addLocation.clicked.connect(self.__add_location_event)
        self.add_location_dialog.ui.progressBar.hide()

        # Add Recordings View
        self.recordings_view = QtWidgets.QDialog()
        self.recordings_view.ui = Ui_RecordingsView()
        self.recordings_view.ui.setupUi(self.recordings_view)

        # Connect UI events to controller_events
        self.ui.actionAdd_New.triggered.connect(self.trigger_add_camera)
        self.ui.actionView_Recordings.triggered.connect(self.trigger_view_recordings)
        self.ui.actionAdd_New_Location.triggered.connect(self.trigger_add_location)
        self.add_camera_dialog.ui.cancel.clicked.connect(self.__cancel_add_camera)
        self.add_location_dialog.ui.cancel.clicked.connect(self.__cancel_add_location)
        self.recordings_view.ui.exit.clicked.connect(self.__exit_recordings_view)
        self.repair_camera_dialog.ui.cancel.clicked.connect(self.__exit_repair_camera_dialog)

        # Start Controller
        self.controller_events["start"](self)

    # Dialog Triggers
    def trigger_view_recordings(self, callback=None):
        self.recordings_view.exec_()
        if callback:
            callback()

    def trigger_add_camera(self, callback=None):
        self.add_camera_dialog.ui.statusBar.setText("")
        self.add_camera_dialog.exec_()
        if callback:
            callback()

    def trigger_add_location(self, callback=None):
        self.add_location_dialog.exec_()
        if callback:
            callback()

    # Internal UI Events
    def __login_event(self):
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

    def __add_camera_event(self):
        self.add_camera_dialog.ui.progressBar.show()
        location_label = self.add_camera_dialog.ui.locationInput.text()
        name = self.add_camera_dialog.ui.nameInput.text()
        protocol = self.add_camera_dialog.ui.protocolInput.text()
        ip = self.add_camera_dialog.ui.ipAddressInput.text()
        path = self.add_camera_dialog.ui.pathInput.text()
        port = self.add_camera_dialog.ui.portInput.text()

        self.add_camera_dialog.ui.locationInput.setDisabled(True)
        self.add_camera_dialog.ui.nameInput.setDisabled(True)
        self.add_camera_dialog.ui.protocolInput.setDisabled(True)
        self.add_camera_dialog.ui.ipAddressInput.setDisabled(True)
        self.add_camera_dialog.ui.pathInput.setDisabled(True)
        self.add_camera_dialog.ui.portInput.setDisabled(True)

        fine = True

        if location_label == '':
            fine = False
            self.add_camera_dialog.ui.locationInput.setStyleSheet('border: 1px solid red;')

        if name == '':
            fine = False
            self.add_camera_dialog.ui.nameInput.setStyleSheet('border: 1px solid red;')

        if protocol == '':
            fine = False
            self.add_camera_dialog.ui.protocolInput.setStyleSheet('border: 1px solid red;')

        if ip == '':
            fine = False
            self.add_camera_dialog.ui.ipAddressInput.setStyleSheet('border: 1px solid red;')

        if path == '':
            fine = False
            self.add_camera_dialog.ui.pathInput.setStyleSheet('border: 1px solid red;')

        if port == '':
            fine = False
            self.add_camera_dialog.ui.portInput.setStyleSheet('border: 1px solid red;')

        if fine:
            success = self.controller_events["add_camera"](location_label, name, ip, port, path, protocol)
            if not success:
                self.add_camera_dialog.ui.statusBar.setText("Failed to add Camera!")
                self.add_camera_dialog.ui.statusBar.setStyleSheet('color: red;')
            # else:
            #     self.add_camera(location_label, "asdfasdfa", name, ip, port, path, protocol)

        self.add_camera_dialog.ui.nameInput.setDisabled(False)
        self.add_camera_dialog.ui.protocolInput.setDisabled(False)
        self.add_camera_dialog.ui.ipAddressInput.setDisabled(False)
        self.add_camera_dialog.ui.pathInput.setDisabled(False)
        self.add_camera_dialog.ui.locationInput.setDisabled(False)
        self.add_camera_dialog.ui.portInput.setDisabled(False)

        self.add_camera_dialog.ui.progressBar.hide()

    def __add_location_event(self):
        self.add_location_dialog.ui.progressBar.show()
        location_label = self.add_location_dialog.ui.locationInput.text()
        fine = True

        if location_label == '':
            fine = False
            self.add_location_dialog.ui.locationInput.setStyleSheet('border: 1px solid red;')

        if fine:
            self.controller_events["add_location"](location_label)

        self.add_location_dialog.ui.locationInput.setDisabled(False)
        self.add_location_dialog.ui.progressBar.hide()

    def __cancel_add_camera(self):
        self.add_camera_dialog.ui.locationInput.setText("")
        self.add_camera_dialog.ui.nameInput.setText("")
        self.add_camera_dialog.ui.protocolInput.setText("rtsp")
        self.add_camera_dialog.ui.ipAddressInput.setText("")
        self.add_camera_dialog.ui.pathInput.setText("")
        self.add_camera_dialog.ui.portInput.setText("")
        self.add_camera_dialog.close()

    def __cancel_add_location(self):
        self.add_location_dialog.ui.locationInput.setText("")
        self.add_location_dialog.close()

    def __exit_recordings_view(self):
        self.recordings_view.close()

    def __repair_camera_event(self):
        self.repair_camera_dialog.ui.progressBar.show()
        location_label = self.repair_camera_dialog.ui.locationInput.text()
        name = self.repair_camera_dialog.ui.nameInput.text()
        protocol = self.repair_camera_dialog.ui.protocolInput.text()
        ip = self.repair_camera_dialog.ui.ipAddressInput.text()
        path = self.repair_camera_dialog.ui.pathInput.text()
        port = self.repair_camera_dialog.ui.portInput.text()

        self.repair_camera_dialog.ui.locationInput.setDisabled(True)
        self.repair_camera_dialog.ui.nameInput.setDisabled(True)
        self.repair_camera_dialog.ui.protocolInput.setDisabled(True)
        self.repair_camera_dialog.ui.ipAddressInput.setDisabled(True)
        self.repair_camera_dialog.ui.pathInput.setDisabled(True)
        self.repair_camera_dialog.ui.portInput.setDisabled(True)

        fine = True

        if location_label == '':
            fine = False
            self.repair_camera_dialog.ui.locationInput.setStyleSheet('border: 1px solid red;')

        if name == '':
            fine = False
            self.repair_camera_dialog.ui.nameInput.setStyleSheet('border: 1px solid red;')

        if protocol == '':
            fine = False
            self.repair_camera_dialog.ui.protocolInput.setStyleSheet('border: 1px solid red;')

        if ip == '':
            fine = False
            self.repair_camera_dialog.ui.ipAddressInput.setStyleSheet('border: 1px solid red;')

        if path == '':
            fine = False
            self.repair_camera_dialog.ui.pathInput.setStyleSheet('border: 1px solid red;')

        if port == '':
            fine = False
            self.repair_camera_dialog.ui.portInput.setStyleSheet('border: 1px solid red;')

        if fine:
            success = self.controller_events["add_camera"](location_label, name, ip, port, path, protocol)
            if not success:
                self.repair_camera_dialog.ui.statusBar.setText("Failed to repair Camera!")
                self.repair_camera_dialog.ui.statusBar.setStyleSheet('color: red;')
            # else:
            #     self.add_camera(location_label, "asdfasdfa", name, ip, port, path, protocol)

        self.repair_camera_dialog.ui.nameInput.setDisabled(False)
        self.repair_camera_dialog.ui.protocolInput.setDisabled(False)
        self.repair_camera_dialog.ui.ipAddressInput.setDisabled(False)
        self.repair_camera_dialog.ui.pathInput.setDisabled(False)
        self.repair_camera_dialog.ui.locationInput.setDisabled(False)
        self.repair_camera_dialog.ui.portInput.setDisabled(False)

        self.repair_camera_dialog.ui.progressBar.hide()

    # UI Manipulation
    def login(self, callback=None):
        self.hide()
        self.login_dialog.exec_()

        if self.loggedIn:
            self.show()
        else:
            self.close()
            sys.exit(0)

    def add_camera(self, location_label, camera_id, name, address, port, path, protocol, callback=None):
        self.camera_elements[camera_id] = {
            "location_label": location_label,
            "name": name,
            "address": address,
            "port": port,
            "path": path,
            "protocol": protocol
        }

        # Add to Location in Tree View:
        camera = QTreeWidgetItem([name])

        location = None
        rowcount = self.ui.locations.topLevelItemCount()
        for i in range(rowcount):
            i = self.ui.locations.topLevelItem(i)
            if location_label == i.text(0):
                location = i
                break

        if location:
            location.addChild(camera)
        else:
            self.ui.locations.addTopLevelItem(QTreeWidgetItem(rowcount))
            self.ui.locations.topLevelItem(rowcount).setText(0, location_label)
            self.ui.locations.topLevelItem(rowcount).addChild(camera)

        # Add StreamView Element
        stream = Ui_StreamView()
        stream.setupUi(stream)
        stream.location.setText(location_label)
        stream.cameraName.setText(name)
        self.camera_elements[camera_id]['stream_view'] = stream
        stream.setMinimumSize(150, 150)
        self.ui.cameras.addWidget(stream, self.camera_elements_row, self.camera_elements_column)

        # Remove 'No Cameras' Prompt
        if ">" in self.ui.promptLabel.text():
            self.ui.promptLabel.setText("")
            self.ui.promptLabel.destroy()

        if self.camera_elements_column != 0 and self.camera_elements_column % 3 == 0:
            self.camera_elements_row += 1
            self.camera_elements_column = 0
        else:
            self.camera_elements_column += 1

    def repair_camera(self, location_label, camera_id, name, address, port, path, protocol):
        self.repair_camera_dialog.ui.locationInput.setText(location_label)
        self.repair_camera_dialog.ui.nameInput.setText(name)
        self.repair_camera_dialog.ui.ipAddressInput.setText(address)
        self.repair_camera_dialog.ui.portInput.setText(port)
        self.repair_camera_dialog.ui.pathInput.setText(path)
        self.repair_camera_dialog.ui.protocolInput.setText(protocol)
        # TODO: Finalise whether the __repair_camera_event calls the add_camera controller function @jordan
        self.repair_camera_dialog.exec_()

    def add_location(self, location_label, callback=None):
        rowcount = self.ui.locations.topLevelItemCount()
        self.ui.locations.addTopLevelItem(QTreeWidgetItem(rowcount))
        self.ui.locations.topLevelItem(rowcount).setText(0, location_label)

    def attach_stream(self, camera_id, stream_object):
        stream_view = self.camera_elements[camera_id]
        stream_object.set_view(stream_view)  # this will now automatically call : stream_view.update(curr

    def update_status(self, message: str, display_for_milliseconds=5000):
        self.ui.statusbar.showMessage(message, display_for_milliseconds)


def log(obj=None):
    print(obj)


app = QtWidgets.QApplication([])
app.setStyle('Breeze')

application = ControlPanel(
    controller_events={
        "start": lambda x: print("Controller: Starting..."),
        "stop": lambda x: print("Controller: Stopping..."),
        "login": lambda username, password: print(
            f'Controller: Logging in {{username: {username}, password: {password}}}') is None,
        "logout": lambda x: print("Controller: Logging out..."),
        "add_camera": lambda location, name, address, port, path, protocol: print(
            f'Controller: Adding Camera - {name}: {{'
            f'protocol: {protocol}, ip: {address}, '
            f'path: {path}, location: {location}}}') is None,
        "remove_camera": lambda id: print(f'Controller: Removing Camera - id: {id}'),
        "add_location": lambda name: print(f'Controller: Adding Location - name: {name}'),
        "remove_location": lambda id: print(f'Controller: Removing Location - id: {id}')
    }
)

# application.show()
application.login(log)
sys.exit(app.exec_())
