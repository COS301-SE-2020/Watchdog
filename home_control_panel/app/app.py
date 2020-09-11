import os
from PyQt5.QtWidgets import QApplication
from .settings import Settings
from .components.component import Component
from .components.layouts.window import Window
from .controller.controller import CameraController
from ..service import services
from ..service.user import User
from .components.popups import LoginPopup


if not os.path.exists('data'):
    os.mkdir('data')
if not os.path.exists('data/temp'):
    os.mkdir('data/temp')
if not os.path.exists('data/temp/video'):
    os.mkdir('data/temp/video')
if not os.path.exists('data/temp/image'):
    os.mkdir('data/temp/image')


class ControlPanel(QApplication, Component):
    def __init__(self):
        super(ControlPanel, self).__init__([])
        self.current_location = ''
        self.settings = Settings()
        self.controller = CameraController(self)
        self.window = Window(self)
        self.login_screen = LoginPopup(self.window)
        self.window.home.view.grid.hide()
        self.window.home.sidepanel.list.hide()
        self.login_screen.show()
        self.setApplicationName("Watchdog Control Panel")

    def user_login(self, username, password):
        print('Logging in...')
        if services.login(username, password):
            self.window.home.view.grid.show()
            self.window.home.sidepanel.list.show()
            self.load_alerts()
            self.load_clips()
            # self.setup()
            return True
        else:
            print('Incorrect Login Details')
        return False

    def setup(self):
        if self.controller.setup_environment():
            if not self.controller.live:
                self.controller.start()

    def change_location(self, location):
        self.current_location = location
        self.window.home.sidepanel.list.button_list.toggle_handler(self.current_location)
        self.window.set_cameras(self.controller.get_cameras(self.current_location))

    # UI Added New Camera
    def add_camera(self, location, name='', address='', port='', path='', protocol=''):
        return self.controller.add_camera(location, name, address, port, path, protocol)

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
        if User.get_instance() is not None:
            self.load_alerts()
            self.window.home.sidepanel.list.toggle()

    def toggle_grid(self):
        if User.get_instance() is not None:
            self.load_clips()
            self.window.home.view.grid.toggle()

    def load_alerts(self):
        log_file = open("data/.logs", "r")
        self.window.home.sidepanel.list.log_list.clear_labels()
        for line in log_file:
            self.window.home.sidepanel.list.log_list.add_label(line)
        log_file.close()

    def load_clips(self):
        for file in os.listdir("data/temp/video"):
            if file.endswith(".mp4"):
                self.window.home.view.grid.retriever.add_view('data/temp/video/' + file)

    def start(self):
        print(self.controller)
        self.window.show()
        self.exec_()

    def end(self):
        self.controller.stop()
        self.controller.join()
        os._exit(1)
