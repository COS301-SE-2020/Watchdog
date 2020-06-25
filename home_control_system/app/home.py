from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QApplication,
    QDesktopWidget
)
from .style import palette
from .containers import Layout


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
        layout = Layout()
        layout.add_cameras(self.cameras)

        widget = QWidget()
        widget.setLayout(layout)

        self.window.setWidget(widget)
        self.window.show()

        self.server.start()
        self.exec_()


class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        sizeObject = QDesktopWidget().screenGeometry(-1)
        self.width = sizeObject.width() / 2
        self.height = sizeObject.height() / 1.66
        self.setGeometry(self.width / 2, sizeObject.height() / 4, self.width, self.height)
        self.setWindowTitle("Home Control Panel")

    def setWidget(self, widget):
        self.setCentralWidget(widget)
