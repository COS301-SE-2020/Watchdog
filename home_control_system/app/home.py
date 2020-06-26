from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QApplication,
    QDesktopWidget
)
from .style import palette
from .component import Component
from .containers import MainLayout


class HomeControlPanel(QApplication):
    def __init__(self, server):
        super(HomeControlPanel, self).__init__([])
        self.setApplicationName("Home Control Panel")
        self.setStyle("Fusion")
        self.setPalette(palette)
        self.server = server
        self.cameras = []

    def add_camera(self, address, port='', path='', location='', protocol=''):
        self.cameras.append(self.server.add_camera(address, port, path, location, protocol))

    def start(self):
        self.window = Window()
        self.window.setLayout(self.cameras)
        self.window.show()

        self.server.start()
        self.exec_()

        while(True):
            for camera in self.cameras:
                camera.visit_stream_view()


class Window(QMainWindow, Component):
    def __init__(self):
        super(Window, self).__init__()
        sizeObject = QDesktopWidget().screenGeometry(-1)
        self.set_dimensions(sizeObject.width() / 2, sizeObject.height() / 1.66)
        self.setGeometry(self.width / 2, sizeObject.height() / 4, self.width, self.height)
        self.setWindowTitle("Home Control Panel")

    def setLayout(self, cameras):
        layout = MainLayout(self)
        layout.add_cameras(cameras)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

