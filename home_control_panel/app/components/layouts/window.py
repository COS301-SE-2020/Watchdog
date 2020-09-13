import os
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import (
    Qt,
    QSize
)
from PyQt5.QtWidgets import (
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLabel
)
from .view import View
from .sidebar import SideBar
from ..component import Component
from ..popups import CameraPopup
from ..style import Style
from ..popups import SettingsPopup
from ..widgets.buttons import PopupButton
from ..widgets.spacers import QVSeperationLine

###############################
# MAIN WINDOW
class Window(QMainWindow, Component):
    def __init__(self, ascendent=None):
        super(Window, self).__init__(ascendent=ascendent)
        self.setStyleSheet(Style.light)

        self.set_dimensions(Style.width, Style.height)
        self.setGeometry(Style.h_margin, Style.v_margin, self.width, self.height)

        self.setMaximumWidth(self.width * 1.2)
        self.setMaximumHeight(self.height * 1.2)

        self.setWindowTitle('Watchdog Control Panel')
        self.setWindowIcon(QIcon('assets/icons/icon.png'))

        self.home = HomeLayout(self)

        self.setCentralWidget(self.home)

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
        self.popup.lbl_warning.show()
        self.popup.show()
###############################


###############################
# MAIN LAYOUT CONTAINER
#   - Side Panel [CONTAINER]
#   - View Panel [CONTAINER]
class HomeLayout(QWidget, Component):
    def __init__(self, ascendent):
        super(HomeLayout, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, self.height)
        self.setContentsMargins(0, 5, 0, 0)
        self.setMinimumWidth(self.width)
        self.setMinimumHeight(self.height)
        self.setMaximumWidth(self.width * 1.2)
        self.setMaximumHeight(self.height * 1.2)

        self.header = HeaderLayout(self)

        # Dark Header
        contain_header = QWidget()
        contain_header.setLayout(self.header)
        contain_header.setStyleSheet(Style.dark)
        contain_header.setStyleSheet(Style.replace_variables('background-color: @LightColor; \
                                                            border-radius: @LargeRadius;'))
        contain_header.setMinimumHeight(int(self.header.height))

        self.sidepanel = SideBar(self)
        contain_panel = QWidget()
        contain_panel.setLayout(self.sidepanel)

        self.view = View(self)
        contain_view = QWidget()
        contain_view.setLayout(self.view)

        lineH = QVSeperationLine()
        lineH.setFixedHeight(self.height / 10)
        lineH.setStyleSheet(Style.replace_variables('background-color: @HighlightColor; \
                                                    border: ' + str(Style.unit / 200) + 'px;'))

        lineO = QVSeperationLine()
        lineO.setFixedHeight(self.height * 8 / 10)
        lineO.setStyleSheet(Style.replace_variables('background-color: @AltLightColor; \
                                                    border: ' + str(Style.unit / 200) + 'px;'))

        line_container = QVBoxLayout()
        line_container.setAlignment(Qt.AlignTop)
        line_container.addStretch(1)
        line_container.addWidget(lineH)
        line_container.addWidget(lineO)

        line_widget = QWidget()
        line_widget.setLayout(line_container)
        line_widget.setStyleSheet('background-color: @AltLightColor;')

        home_layout = QHBoxLayout()
        home_layout.setAlignment(Qt.AlignCenter)
        home_layout.setContentsMargins(0, 0, 0, 0)
        home_layout.setSpacing(0)

        home_layout.addWidget(contain_panel)
        home_layout.addWidget(line_widget)
        home_layout.addWidget(contain_view)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(contain_header, 1)
        main_layout.addLayout(home_layout, 7)

        self.setLayout(main_layout)

    def add_camera(self, camera):
        self.view.grid.add_stream_view(camera)


class HeaderLayout(QHBoxLayout, Component):
    def __init__(self, ascendent):
        super(HeaderLayout, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height * 0.1))
        self.setContentsMargins(0, 0, 0, 0)
        self.setAlignment(Qt.AlignCenter)

        self.icon_logo = QLabel()
        self.icon_header = QLabel()

        map_logo = QPixmap('assets/icons/icon.png')
        self.icon_logo.setFixedHeight(self.height)
        self.icon_logo.setPixmap(map_logo.scaled(Style.sizes.icon_logo, self.height * 0.8, Qt.KeepAspectRatio, Qt.FastTransformation))
        self.icon_logo.setContentsMargins(int(Style.unit / 8), 0, int(Style.unit / 16), 0)

        self.lbl_header = QLabel()
        self.lbl_header.setText('CONTROL PANEL')
        self.lbl_header.setStyleSheet(Style.replace_variables('font: @HeadTextSize @TextFont; \
                                                                font-weight: 50;'))

        map_settings = QPixmap('assets/icons/settings.png')
        self.btn_settings = PopupButton(self, SettingsPopup)
        self.btn_settings.setIcon(QIcon(map_settings))
        self.btn_settings.setIconSize(QSize(Style.sizes.icon_medium, Style.sizes.icon_medium))

        self.addStretch(1)
        self.addWidget(self.icon_logo)
        self.addStretch(1)
        self.addWidget(self.lbl_header, Qt.AlignLeft)
        self.addStretch(20)
        self.addWidget(self.btn_settings, Qt.AlignRight)
        self.addStretch(1)

    def toggle_login(self):
        Component.root.login_screen.show()
###############################
