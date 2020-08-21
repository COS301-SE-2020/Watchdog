from PyQt5.QtWidgets import QApplication
from .settings import Settings
from .components.component import Component
from .components.layouts.window import Window
from .controller.controller import CameraController
from service import services


class ControlPanel(QApplication, Component):
    def __init__(self):
        super(ControlPanel, self).__init__([])
        self.settings = Settings()
        self.controller = CameraController(self)
        self.window = Window(self)
        self.current_location = ''
        self.setApplicationName("Watchdog Control Panel")

    def user_login(self, username, password):
        print('Logging in...')
        if services.login(username, password):
            if self.controller.setup_environment():
                self.controller.start()
        else:
            print('Incorrect Login Details')

    def change_location(self, location):
        self.current_location = location
        self.window.home.sidepanel.list.button_list.toggle_handler(self.current_location)
        self.window.set_cameras(self.controller.get_cameras(self.current_location))

    # UI Added New Camera
    def add_camera(self, location, address, port='', path='', protocol=''):
        return self.controller.add_camera(location, address, port, path, protocol)

    # UI Added New Location
    def add_location(self, location):
        return self.controller.add_location(location)

    # Return Camera Info for UI
    def get_cameras(self, location):
        return self.controller.get_cameras(location)

    # Return Location Info for UI
    def get_locations(self):
        return self.controller.get_locations()

    # Return Resolution Info for UI
    def get_resolution(self):
        screen_resolution = self.desktop().screenGeometry()
        return (screen_resolution.width(), screen_resolution.height())

    def toggle_list(self):
        self.window.home.sidepanel.list.toggle()

    def toggle_grid(self):
        self.window.home.view.grid.toggle()

    def start(self):
        print(self.controller)
        self.window.show()
        self.exec_()
