import time
from PyQt5.QtWidgets import QApplication
from .containers import Window
from .component import Component
from .styles import style_light

class HomeControlPanel(QApplication, Component):
    def __init__(self, server):
        super(HomeControlPanel, self).__init__([])
        self.cameras = []
        self.server = server
        self.setApplicationName("Home Control Panel (Watchdog)")
        self.setStyle("Fusion")
        self.setStyleSheet(style_light)

    def add_camera(self, address, port='', path='', location='', protocol=''):
        self.cameras.append(self.server.add_camera(address, port, path, location, protocol))

    def get_resolution(self):
        screen_resolution = self.desktop().screenGeometry()
        return (screen_resolution.width(), screen_resolution.height())

    def start(self):
        print(self.server)
        time.sleep(1)
        self.server.start()
        self.window = Window(self)
        self.window.buildLayout(self.cameras)
        self.window.show()
        self.exec_()
        while(True):
            for camera in self.cameras:
                camera.visit_stream_view()
