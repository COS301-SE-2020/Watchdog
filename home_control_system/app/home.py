import time
from PyQt5.QtWidgets import QApplication
from .containers import Window
from .component import Component
from .styles import Style

class HomeControlPanel(QApplication, Component):
    def __init__(self, server):
        super(HomeControlPanel, self).__init__([])
        self.cameras = []
        self.locations = []
        self.server = server
        self.setApplicationName("Home Control Panel (Watchdog)")

        (width, height) = self.get_resolution()
        Style.set_unit((width / 2) / 5)
        self.setStyle('Fusion')
        self.window = Window(self)

    def add_camera(self, id, address, port='', path='', location='', protocol=''):
        camera = self.server.add_camera(id, address, port, path, location, protocol)
        self.cameras.append(camera)
        self.window.addCamera(camera)

    def add_location(self, id, location):
        self.locations.append((id, location))
        self.window.addLocation(location)

    def get_resolution(self):
        screen_resolution = self.desktop().screenGeometry()
        return (screen_resolution.width(), screen_resolution.height())

    def start(self):
        print(self.server)
        time.sleep(1)
        self.server.start()
        self.window.show()
        self.exec_()

        while(True):
            for camera in self.cameras:
                camera.visit_stream_view()
