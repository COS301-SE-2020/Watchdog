import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy
)
from ..component import Component
from ..popups import CameraPopup
from ..style import Style
from ..widgets.spacers import (
    QHSeperationLine,
    QVSeperationLine
)
from .sidebar import SideBar
from .view import View


###############################
# MAIN WINDOW
class Window(QMainWindow, Component):
    def __init__(self, ascendent=None):
        super(Window, self).__init__(ascendent=ascendent)
        self.setStyleSheet(Style.dark)

        self.set_dimensions(5.5 * Style.unit, 3 * Style.unit)
        self.setGeometry(int((5 * Style.unit) / 2), int(self.height / 2), self.width, self.height)

        self.setWindowTitle('Watchdog Control Panel')
        self.setWindowIcon(QIcon('assets/icons/watchdog_white.png'))

        self.home = HomeLayout(self)
 
        home_container = QWidget()
        home_container.setMinimumWidth(self.width)
        home_container.setLayout(self.home)

        spacer = QSpacerItem(self.width, int(Style.unit / 8), QSizePolicy.Fixed)
        line = QHSeperationLine()
        line.setStyleSheet(Style.replace_variables(('background-color:black;')))

        layout = QVBoxLayout()
        layout.addSpacerItem(spacer)
        layout.addWidget(line)
        layout.addWidget(home_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        contain_layout = QWidget()
        contain_layout.setLayout(layout)
        contain_layout.setMinimumWidth(self.width)

        self.setCentralWidget(contain_layout)

    def closeEvent(self, event):
        event.accept()  # let the window close
        sys.exit()

    def set_locations(self, labels):
        self.home.sidepanel.list.clear()
        for label in labels:
            self.home.sidepanel.list.add_button(label)

    def set_cameras(self, cameras):
        self.home.view.grid.set_stream_views(cameras)

    def fix_camera(self, label, address, port, protocol, path):
        self.popup = CameraPopup(ascendent=self, label=label, address=address, port=port, protocol=protocol, path=path)
        self.popup.show()
###############################


###############################
# MAIN LAYOUT CONTAINER
#   - Side Panel [CONTAINER]
#   - View Panel [CONTAINER]
class HomeLayout(QHBoxLayout, Component):
    def __init__(self, ascendent):
        super(HomeLayout, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        self.sidepanel = SideBar(self)

        contain_panel = QWidget()
        contain_panel.setLayout(self.sidepanel)
        contain_panel.setMinimumWidth(self.width * 1/5)
        contain_panel.setMaximumWidth(self.width * 6/10)

        self.view = View(self)

        contain_view = QWidget()
        contain_view.setLayout(self.view)
        contain_view.setMinimumWidth(self.width * 4/5)
        contain_view.setMaximumWidth(self.width * 12/5)

        line = QVSeperationLine()
        line.setStyleSheet(Style.replace_variables('background-color:black;'))

        self.addWidget(contain_panel, 1)
        self.addWidget(line)
        self.addWidget(contain_view, 4)

    def add_camera(self, camera):
        self.view.grid.add_stream_view(camera)
###############################