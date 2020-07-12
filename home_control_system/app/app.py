import threading
import time
from PyQt5.QtWidgets import QApplication
from .containers import Window
from .component import Component

class HomeControlPanel(QApplication, Component):
    def __init__(self, server):
        super(HomeControlPanel, self).__init__([])
        self.list = None
        self.server = server
        self.window = Window(self)
        self.list = LocationList(self.window)
        self.setApplicationName("Watchdog Control Panel")
        self.setStyle('Fusion')

    def user_login(self, username, password):
        print('Logging in')
        # TODO: Perform login here

    def add_camera(self, address, port='', path='', location='', protocol=''):
        return self.list.add_camera(address, port, path, location, protocol)

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
        time.sleep(1)
        self.window.show()
        self.list.start()
        self.exec_()


class Location:
    # Number reserved ports (for if we serve it)
    camera_spaces = 20

    def __init__(self, id, location):
        self.id = id
        self.label = location
        self.cameras = []

    def add_camera(self, id, address, port='', path='', location='', protocol=''):
        camera = Component.root.server.add_camera(id, address, port, path, location, protocol)
        self.cameras.append(camera)
        return camera


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

        # TODO: update location in database

        return location

    def add_camera(self, address, port='', path='', location='', protocol=''):
        if self.index > len(self.locations):
            return None

        camera = self.locations[self.index].add_camera((self.index * Location.camera_spaces) + len(self.locations[self.index].cameras), address, port, path, location, protocol)

        if self.view is not None:
            self.view.home.view.grid.set_stream_views(self.locations[self.index].cameras)

        # TODO: update camera in database

        return camera

    def changeActive(self, index):
        self.index = index
        self.view.home.view.grid.set_stream_views(self.locations[self.index].cameras)
