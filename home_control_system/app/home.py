import time
from PyQt5.QtWidgets import QApplication
from .containers import Window
from .style import palette


class HomeControlPanel(QApplication):
    def __init__(self, server):
        super(HomeControlPanel, self).__init__([])
        self.cameras = []
        self.server = server
        self.setStyle("Fusion")
        self.setPalette(palette)
        self.setApplicationName("Home Control Panel")

    def add_camera(self, address, port='', path='', location='', protocol=''):
        self.cameras.append(self.server.add_camera(address, port, path, location, protocol))

    def start(self):
        print(self.server)
        time.sleep(1)
        self.server.start()
        self.window = Window()
        self.window.buildLayout(self.cameras)
        self.window.show()
        self.exec_()
        while(True):
            for camera in self.cameras:
                camera.visit_stream_view()
