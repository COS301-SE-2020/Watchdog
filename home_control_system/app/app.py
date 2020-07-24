import threading
import time
from PyQt5.QtWidgets import QApplication
from .containers import Window
from .component import Component
from .settings import Settings
from .controller.controller import CameraController
from service import services


class HomeControlPanel(QApplication, Component):
    def __init__(self):
        super(HomeControlPanel, self).__init__([])
        self.settings = Settings()
        self.list = None
        self.controller = CameraController()
        self.window = Window(self)
        self.list = LocationList(self.window)
        self.setApplicationName("Watchdog Control Panel")

    def user_login(self, username, password):
        print('Logging in...')
        services.login(username, password)
        self.setup_environment()

    def setup_environment(self):
        print('Loading Environment...')
        locations = services.get_location_setup()
        cameras = services.get_camera_setup()
        count = 0
        if locations is not None:
            for location in locations:
                self.list.add_location(location)
                if cameras is not None:
                    for camera_id in cameras:
                        camera = cameras[camera_id]
                        if camera['room'] == location:
                            camera = self.list.add_camera(camera['address'], camera['port'], camera['path'], camera['protocol'], upload=False, index=count)
                            if camera is not None:
                                camera.id = camera_id
                count += 1

    def add_camera(self, address, port='', path='', protocol=''):
        return self.list.add_camera(address, port, path, protocol)

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
        self.controller.start()
        self.window.show()
        self.list.start()
        self.exec_()


class Location:
    count = 0

    def __init__(self, location):
        self.id = Location.count
        self.label = location
        self.cameras = []
        Location.count += 1

    def add_camera(self, address, port='', path='', protocol=''):
        camera = Component.root.controller.add_camera(address, port, path, self.label, protocol)
        if camera is not None:
            self.cameras.append(camera)
        return camera

    def get_metadata(self):
        camera_list = ''
        for index in range(len(self.cameras)):
            camera_list += str(self.cameras.id)
        return {
            "location": self.label,
            "cameras": camera_list
        }


class LocationList(threading.Thread):
    def __init__(self, view=None):
        threading.Thread.__init__(self)
        self.locations = []
        self.view = view
        self.index = 0

    def run(self):
        while(True):
            self.view.home.view.grid.viewer.refresh()
            time.sleep(1 / 30)  # 30 fps

    def add_location(self, label):
        location = Location(label)

        self.index = Location.count

        self.locations.append(location)

        if self.view is not None:
            self.view.home.sidepanel.list.add_button(label)

        return location

    def add_camera(self, address, port='', path='', protocol='', upload=True, index=-1):
        if self.index > len(self.locations) - 1:
            return None

        if index != -1:
            self.index = index
        camera = self.locations[self.index].add_camera(
            address,
            port,
            path,
            protocol
        )

        if camera is not None and camera.is_connected:
            if self.view is not None:
                self.view.home.view.grid.set_stream_views(self.locations[self.index].cameras)

            if upload:
                response = services.upload_camera(camera.id, camera.get_metadata())
                if response is not None and response.status_code != 200:
                    return None

            return camera
        return None

    def changeActive(self, index):
        self.index = index
        self.view.home.view.grid.set_stream_views(self.locations[self.index].cameras)
