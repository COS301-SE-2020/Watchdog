import os
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (
    Qt
)
from PyQt5.QtWidgets import (
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QGraphicsDropShadowEffect
)
from ..component import Component
from ..popups import CameraPopup
from ..style import Style
from ..widgets.spacers import (
    QVSeperationLine
)
from .sidebar import SideBar
from .view import View


###############################
# MAIN WINDOW
class Window(QMainWindow, Component):
    def __init__(self, ascendent=None):
        super(Window, self).__init__(ascendent=ascendent)
        self.setStyleSheet(Style.light)

        self.set_dimensions(Style.width, Style.height)
        self.setGeometry(Style.h_margin, Style.v_margin, self.width, self.height)

        self.setWindowTitle('Watchdog Control Panel')
        self.setWindowIcon(QIcon('assets/icons/icon.png'))

        self.home = HomeLayout(self)

        home_container = QWidget()
        home_container.setMinimumWidth(self.width)
        home_container.setLayout(self.home)

        layout = QVBoxLayout()
        layout.addWidget(home_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        contain_layout = QWidget()
        contain_layout.setLayout(layout)
        contain_layout.setMinimumWidth(self.width)

        self.setCentralWidget(contain_layout)

    def closeEvent(self, event):
        Component.root.controller.client.socket.disconnect()
        os._exit(1)

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
        self.setAlignment(Qt.AlignTop)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        self.sidepanel = SideBar(self)

        contain_panel = QWidget()
        contain_panel.setLayout(self.sidepanel)
        contain_panel.setMinimumWidth(self.width * 1 / 6)
        contain_panel.setMaximumWidth(self.width * 6 / 10)

        contain_panel.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=6, xOffset=3, yOffset=3))

        self.view = View(self)

        contain_view = QWidget()
        contain_view.setLayout(self.view)
        contain_view.setMinimumWidth(self.width * 5 / 6)
        contain_view.setMaximumWidth(self.width * 12 / 5)

        lineH = QVSeperationLine()
        lineH.setStyleSheet(Style.replace_variables('background-color: @HighlightColor; border: ' + str(Style.unit / 200) + 'px;'))
        lineH.setFixedHeight(self.height / 10 * 0.6)

        line_container = QVBoxLayout()
        line_container.setAlignment(Qt.AlignTop)
        line_container.addStretch(1)
        line_container.addWidget(lineH)
        line_container.addStretch(10)
        line_container.addStretch(35)

        self.addWidget(contain_panel, 1)
        self.addLayout(line_container)
        self.addWidget(contain_view, 5)

    def add_camera(self, camera):
        self.view.grid.add_stream_view(camera)
###############################
