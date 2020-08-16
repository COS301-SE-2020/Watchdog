import random
from hashlib import sha256
from PyQt5.QtWidgets import QApplication
from .containers import Window
from .component import Component
from .settings import Settings
from .controller.controller import CameraController
from .controller.location import LocationList
from service import services


class HomeControlPanel(QApplication, Component):
    def __init__(self):
        super(HomeControlPanel, self).__init__([])
        self.list = None  # needed
        self.settings = Settings()
        self.controller = CameraController()
        self.window = Window(self)
        self.list = LocationList(self.window)
        self.setApplicationName("Watchdog Control Panel")

    def user_login(self, username, password):
        print('Logging in...')
        if services.login(username, password):
            # self.controller.start()
            self.list.start()
            self.setup_environment()
            self.controller.start()
        else:
            print('Incorrect Login Details')

    def setup_environment(self):
        print('Loading Environment...')
        count = 0
        locations = services.get_camera_setup()
        if locations is not None:
            for location, cameras in locations.items():
                count += 1
                self.list.add_location(location)
                if cameras is not None:
                    for camera_id, camera in cameras.items():
                        print(camera)
                        camera = self.list.add_camera(
                            camera_id,
                            camera['address'],
                            camera['port'],
                            camera['path'],
                            camera['protocol'],
                            upload=False
                        )
                        if camera is not None:
                            camera.id = camera_id

    def add_camera(self, address, port='', path='', protocol=''):
        id = 'c' + str(sha256((str(random.getrandbits(128))).encode('ascii')).hexdigest())
        return self.list.add_camera(id, address, port, path, protocol)

    def add_location(self, location):
        return self.list.add_location(location)

    def get_cameras(self):
        if self.list is None:
            return None
        if self.list.index >= len(self.list.locations):
            return []
        return self.list.locations[self.list.index].cameras

    def get_locations(self):
        if self.list is not None:
            return self.list.locations
        return []

    def get_resolution(self):
        screen_resolution = self.desktop().screenGeometry()
        return (screen_resolution.width(), screen_resolution.height())

    def start(self):
        print(self.controller)
        self.window.show()
        self.exec_()
