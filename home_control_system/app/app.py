import threading
import time
from PyQt5.QtWidgets import QApplication
from .containers import Window
from .component import Component
from service import (
    config,
    services
)


class HomeControlPanel(QApplication, Component):
    def __init__(self, server):
        super(HomeControlPanel, self).__init__([])
        self.list = None
        self.server = server
        self.window = Window(self)
        self.list = LocationList(self.window)
        self.setApplicationName("Watchdog Control Panel")
        self.setStyle('Fusion')
        self.setup_environment()

    def user_login(self, username, password):
        print('Logging in...')
        services.login(username, password)

    def setup_environment(self):
        print('Loading Environment...')
        locations = services.get_location_setup()
        cameras = services.get_camera_setup()
        for location in locations:
            self.add_location(location)
            for camera in cameras:
                if camera['location'] == location:
                    self.add_camera(camera['address'], camera['port'], camera['path'], camera['protocol'])

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
        print(self.server)
        self.server.start()
        self.window.show()
        self.list.start()
        self.exec_()


class Location:
    def __init__(self, id, location):
        self.id = id
        self.label = location
        self.cameras = []

    def add_camera(self, address, port='', path='', protocol=''):
        camera = Component.root.server.add_camera(address, port, path, self.label, protocol)
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
        self.index = len(self.locations)

        location = Location(self.index, label)

        self.locations.append(location)

        if self.view is not None:
            self.view.home.sidepanel.list.add_button(label)

        return location

    def add_camera(self, address, port='', path='', protocol=''):
        if self.index > len(self.locations):
            return None

        camera = self.locations[self.index].add_camera(
            address,
            port,
            path,
            protocol
        )

        if self.view is not None:
            self.view.home.view.grid.set_stream_views(self.locations[self.index].cameras)

        # TODO: Update camera in database ~INTEGRATION~
        response = services.upload_camera(camera.id, camera.get_metadata())
        if response is not None and response.status_code != 200:
            return None
        return camera

    def changeActive(self, index):
        self.index = index
        self.view.home.view.grid.set_stream_views(self.locations[self.index].cameras)
