import os
import sys
from time import sleep

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTreeWidgetItem, QFileSystemModel
from home_control_panel.app.frontend.Interface import Interface
from home_control_panel.app.frontend.gui.add_camera_dialog import Ui_AddCamera
from home_control_panel.app.frontend.gui.add_location_dialog import Ui_AddLocation
from home_control_panel.app.frontend.gui.login_dialog import Ui_Login
from home_control_panel.app.frontend.gui.main_window import Ui_MainWindow
from home_control_panel.app.frontend.gui.recordings_view import Ui_RecordingsView
from home_control_panel.app.frontend.gui.repair_camera_dialog import Ui_RepairCamera
from home_control_panel.app.frontend.gui.stream_view import Ui_StreamView
from ..service import services
from ..service.settings import Settings
from .controller.controller import CameraController


class ControlPanel(QtWidgets.QMainWindow, Interface):
    def __init__(self, controller_events: dict):
        super().__init__(controller_events=controller_events)
        self.loggedIn = False

        self.camera_elements_row = 0
        self.camera_elements_column = 0
        self.locations = []
        self.camera_elements = {}
        self.location_elements = {}

        self.settings = Settings()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.progressBar.hide()

        # Login Dialog
        self.login_dialog = QtWidgets.QDialog()
        self.login_dialog.ui = Ui_Login()
        self.login_dialog.ui.setupUi(self.login_dialog)
        # self.login_dialog.ui.progressBar.hide()
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
        model = QFileSystemModel()
        model.setRootPath('~')  # TODO: Please set this to the directory path of the recordings @Jordan
        self.recordings_view.ui.directory.setModel(model)

        # Connect UI events to controller_events
        self.ui.actionAdd_New.triggered.connect(self.trigger_add_camera)
        self.ui.actionView_Recordings.triggered.connect(self.trigger_view_recordings)
        self.ui.actionAdd_New_Location.triggered.connect(self.trigger_add_location)
        self.add_camera_dialog.ui.cancel.clicked.connect(self.__cancel_add_camera)
        self.add_location_dialog.ui.cancel.clicked.connect(self.__cancel_add_location)
        self.recordings_view.ui.exit.clicked.connect(self.__exit_recordings_view)
        self.repair_camera_dialog.ui.cancel.clicked.connect(self.__exit_repair_camera_dialog)

        # Start Controller
        self.controller_events["start"]()

    # Dialog Triggers
    def trigger_view_recordings(self, callback=None):
        self.recordings_view.exec_()
        if callback:
            callback()

    def trigger_add_camera(self, callback=None):
        self.add_camera_dialog.ui.statusBar.setText("")
        if len(self.locations) == 0:
            self.trigger_add_location()

        self.add_camera_dialog.ui.locationInput.clear()
        self.add_camera_dialog.ui.locationInput.addItems(self.locations)
        self.add_camera_dialog.exec_()
        if callback:
            callback()

    def trigger_add_location(self, callback=None):
        self.add_location_dialog.exec_()
        if callback:
            callback()

    # Internal UI Events
    def __login_event(self):
        self.login_dialog.ui.statusBar.setText("Logging in...")
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
                self.login_dialog.ui.statusBar.setText("Success!")
                self.login_dialog.close()
            else:
                self.login_dialog.ui.statusBar.setText('Login Failed. Please Check Credentials...')

        self.login_dialog.ui.usernameInput.setDisabled(False)
        self.login_dialog.ui.passwordInput.setDisabled(False)
        self.login_dialog.ui.progressBar.hide()

    def __add_camera_event(self):
        self.add_camera_dialog.ui.statusBar.setText(f"Adding Camera {self.add_camera_dialog.ui.nameInput.text()}...")
        self.add_camera_dialog.ui.progressBar.show()
        location_label = str(self.add_camera_dialog.ui.locationInput.currentText())
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
            camera = self.controller_events["add_camera"](location_label, name, ip, port, path, protocol)

            if camera is None:
                self.add_camera_dialog.ui.statusBar.setText("Failed to add Camera!")
                self.add_camera_dialog.ui.statusBar.setStyleSheet('color: red;')
            else:
                self.add_camera(location_label, camera.id, name, ip, port, path, protocol)
                self.attach_stream(camera.id, camera.stream)

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
            self.add_location(location_label)

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

    def __exit_repair_camera_dialog(self):
        self.repair_camera_dialog.close()

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
            camera = self.controller_events["add_camera"](location_label, name, ip, port, path, protocol)

            if camera is None:
                self.repair_camera_dialog.ui.statusBar.setText("Failed to repair Camera!")
                self.repair_camera_dialog.ui.statusBar.setStyleSheet('color: red;')
            else:
                self.add_camera(location_label, camera.id, name, ip, port, path, protocol)
                self.attach_stream(camera.id, camera.stream)
                self.repair_camera_dialog.hide()

        self.repair_camera_dialog.ui.nameInput.setDisabled(False)
        self.repair_camera_dialog.ui.protocolInput.setDisabled(False)
        self.repair_camera_dialog.ui.ipAddressInput.setDisabled(False)
        self.repair_camera_dialog.ui.pathInput.setDisabled(False)
        self.repair_camera_dialog.ui.locationInput.setDisabled(False)
        self.repair_camera_dialog.ui.portInput.setDisabled(False)

        self.repair_camera_dialog.ui.progressBar.hide()

    def __remove_camera(self, camera_id):
        self.camera_elements[camera_id]['stream_view'].destroy()
        self.camera_elements[camera_id]['stream_view'].deleteLater()
        camera_location = self.camera_elements[camera_id]['location_view']
        location_label = self.camera_elements[camera_id]['location_label']
        self.location_elements[location_label]['location_view'].removeChild(camera_location)
        self.update()

    # UI Manipulation
    def login(self, callback=None):
        self.hide()
        self.login_dialog.ui.progressBar.hide()
        self.login_dialog.exec_()
        if self.loggedIn:
            self.show()
            self.ui.progressBar.show()
            self.update()
            self.update_status("Start Environment Loadup...", None)
            # sleep(5)
            self.setup_environment()
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
        self.camera_elements[camera_id]['location_view'] = camera

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
        stream.camera_id = camera_id
        stream.location.setText(location_label)
        stream.cameraName.setText(name)

        # Connect dynamic events
        stream.removeStream.clicked.connect(lambda: self.remove_camera(stream.camera_id))
        stream.pauseStream.clicked.connect(lambda: self.pause_stream(stream.camera_id))
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
        self.repair_camera_dialog.exec_()

    def add_location(self, location_label, callback=None):
        self.locations.append(location_label)
        rowcount = self.ui.locations.topLevelItemCount()
        self.location_elements[location_label] = {}
        self.location_elements[location_label]['location_view'] = QTreeWidgetItem(rowcount)
        self.ui.locations.addTopLevelItem(self.location_elements[location_label]['location_view'])
        self.ui.locations.topLevelItem(rowcount).setText(0, location_label)

    def attach_stream(self, camera_id, stream_object):
        stream_view = self.camera_elements[camera_id]['stream_view']
        stream_object.set_view(stream_view)  # this will now automatically call : stream_view.update(curr

    def update_status(self, message: str, display_for_milliseconds=5000):
        if display_for_milliseconds is None:
            self.ui.statusbar.showMessage(message)
        else:
            self.ui.statusbar.showMessage(message, display_for_milliseconds)
        self.update()

    def remove_camera(self, camera_id, callback=None):
        # TODO: We need to basically call controller["remove_camera"] and then __remove_camera (like bellow) on success @Jordan
        self.__remove_camera(camera_id)

    def pause_stream(self, camera_id):
        # TODO: Please connect this to controller @Jordan
        pass

    def detected_face_on(self, camera_id):
        self.camera_elements[camera_id]['stream_view'].detectedLabel.setStyle('color: red;')

    def detected_face_off(self, camera_id):
        self.camera_elements[camera_id]['stream_view'].detectedLabel.setStyle('color: green;')

    # Called at Start, Pass in UI Window for UI Setup
    def setup_environment(self):
        print('Loading Environment...')
        self.update_status("Environment: Getting Camera Setup...")
        try:
            locations = services.get_camera_setup()
            if locations is not None:
                for location, cameras in locations.items():
                    self.update_status("Environment: Loading Locations...")
                    controller.load_location(location)
                    self.add_location(location)
                    if cameras is not None:
                        for camera_id, camera in cameras.items():
                            self.update_status(f"Environment: Loading Camera {camera['name']}...")
                            loaded_camera = controller.load_camera(
                                location,
                                camera_id,
                                camera['name'],
                                camera['address'],
                                camera['port'],
                                camera['path'],
                                camera['protocol']
                            )
                            # Camera Failed to Connect, Delete from DB and Ask User to Fix Details
                            if loaded_camera is None:
                                self.update_status(
                                    f"Environment: Camera {camera['name']} broken. Attempting Repair...")
                                services.remove_camera(location, camera_id)
                                self.repair_camera(location, camera_id, camera['name'], camera['address'],
                                                   camera['port'], camera['path'], camera['protocol'])
                            else:
                                self.update_status(f"Environment: Camera {camera['name']} loaded.")
                                self.add_camera(location, camera_id, camera['name'], camera['address'], camera['port'],
                                                camera['path'], camera['protocol'])
                                self.update_status(
                                    f"Environment: Attaching Stream from Camera {camera['name']}....")
                                self.attach_stream(loaded_camera.id, loaded_camera.stream)
                                self.update_status(
                                    f"Environment: Done Attaching Stream from Camera {camera['name']}....")
                self.ui.statusbar.showMessage("Ready")
                self.ui.progressBar.hide()
        except Exception as e:
            print('error occured!!')
            self.ui.statusbar.showMessage("Environment Failed to load!!")
            print(e)

        self.ui.statusbar.showMessage("Ready")
        self.ui.progressBar.hide()
        return False


def log(obj=None):
    print(obj)


app = QtWidgets.QApplication([])
app.setStyle('Breeze')

controller = CameraController()
application = ControlPanel(
    controller_events={
        "start": lambda: controller.start(),
        "stop": lambda: controller.stop(),
        "login": lambda username, password: services.login(username, password),
        "logout": lambda x: print("Controller: Logging out..."),
        "add_camera": lambda location, name, address, port, path, protocol: controller.add_camera(location, name,
                                                                                                  address, port, path,
                                                                                                  protocol),
        "remove_camera": lambda id: controller.remove_camera(id),
        "add_location": lambda name: controller.add_location(name),
        "remove_location": lambda id: controller.remove_location(id)
    }
)

application.login(log)
