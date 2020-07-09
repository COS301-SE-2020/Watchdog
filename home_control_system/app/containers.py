import sys
from PyQt5.QtCore import (
    Qt,
    QSize
)
from PyQt5.QtGui import (
    QIcon,
    QPixmap
)
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QScrollArea,
    QGraphicsDropShadowEffect
)
from .widgets import (
    StreamGrid,
    ButtonList,
    PopupButton,
    SettingsPopup,
    PanelToggle,
    CenterToggle,
    QVSeperationLine,
    QHSeperationLine
)
from .component import Component
from .styles import Style


###############################
# MAIN WINDOW
class Window(QMainWindow, Component):
    def __init__(self, ascendent=None):
        super(Window, self).__init__(ascendent=ascendent)
        self.setStyleSheet(Style.dark)

        self.set_dimensions(5.5 * Style.unit, 3 * Style.unit)
        self.setGeometry(int((5 * Style.unit) / 2), int(self.height / 2), self.width, self.height)

        self.setWindowTitle('Home Control Panel')
        self.setWindowIcon(QIcon('assets/icons/watchdog_white.png'))
        self.setWindowFlags(Qt.WindowFlags(Qt.FramelessWindowHint))

        self.home = HomeContainer(self)

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

    def addCamera(self, camera):
        self.home.add_camera(camera)
    
    def addLocation(self, location):
        self.home.sidepanel.list.add_button(location)

    def closeEvent(self, event):
        event.accept()  # let the window close
        sys.exit()
###############################


###############################
# MAIN LAYOUT CONTAINER
#   - Side Panel [CONTAINER]
#   - View Panel [CONTAINER]
class HomeContainer(QHBoxLayout, Component):
    def __init__(self, ascendent):
        super(HomeContainer, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        self.sidepanel = SidePanelContainer(self)

        contain_panel = QWidget()
        contain_panel.setLayout(self.sidepanel)
        contain_panel.setMinimumWidth(self.width * 1/5)
        contain_panel.setMaximumWidth(self.width * 6/10)

        self.view = ViewPanelContainer(self)

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


###############################
# SIDE PANEL CONTAINER
#   - Side Header Container [CONTAINER]
#   - List Toggle [CONTAINER]
class SidePanelContainer(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(SidePanelContainer, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width / 5, self.height)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
        self.setAlignment(Qt.AlignLeft)

        self.header = SideHeaderContainer(self)
        self.list = SideListToggleContainer(self)

        # Dark Header
        contain_location = QWidget()
        contain_location.setLayout(self.header)
        contain_location.setStyleSheet(Style.light)
        contain_location.setMinimumHeight(int(self.header.height))
        contain_location.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))

        line_h = QHSeperationLine()
        line_h.setStyleSheet(Style.replace_variables('background-color:black;'))

        line_v = QVSeperationLine()
        line_v.setStyleSheet(Style.replace_variables('background-color:black;'))

        line_alt = QVSeperationLine()
        line_alt.setStyleSheet(Style.replace_variables('background-color:white;'))

        holder_layout_top = QHBoxLayout()
        holder_layout_top.addWidget(contain_location)
        holder_layout_top.addWidget(line_v)

        holder_layout_bottom = QHBoxLayout()
        holder_layout_bottom.addLayout(self.list)
        holder_layout_bottom.addWidget(line_alt)

        self.addLayout(holder_layout_top, 4)
        self.addWidget(line_h)
        self.addLayout(holder_layout_bottom, 22)
# SIDE HEADER CONTAINER
#   - Home Icon [WIDGET]
#   - Location Label [WIDGET]
#   - Settings Button [WIDGET]
class SideHeaderContainer(QHBoxLayout, Component):
    def __init__(self, ascendent):
        super(SideHeaderContainer, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height / 26) * 4)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
        self.setAlignment(Qt.AlignLeft)

        self.icon_home = QLabel()
        self.lbl_location = QLabel()
        self.btn_settings = PopupButton(self, SettingsPopup)

        map_home = QPixmap('assets/icons/home.png')
        self.icon_home.setPixmap(map_home.scaled(Style.sizes.icon_medium, Style.sizes.icon_medium, Qt.KeepAspectRatio, Qt.FastTransformation))
        self.lbl_location.setText('Home')
        map_settings = QPixmap('assets/icons/settings.png')
        self.btn_settings.setIcon(QIcon(map_settings))
        self.btn_settings.setIconSize(QSize(Style.sizes.icon_medium, Style.sizes.icon_medium))

        self.icon_home.setContentsMargins(int(Style.unit / 8), 0, int(Style.unit / 24), 0)
        self.btn_settings.setContentsMargins(0, 0, int(Style.unit / 8), 0)

        self.addWidget(self.icon_home)
        self.addWidget(self.lbl_location)
        self.addStretch(1)
        self.addWidget(self.btn_settings, Qt.AlignRight)

        # self.btn_settings.clicked.connect(show_popup())
# SIDE LIST TOGGLE CONTAINER
#   - Button Toggle [WIDGET]
#   - Button List [WIDGET]
class SideListToggleContainer(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(SideListToggleContainer, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height / 26) * 23)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        self.list_toggle = PanelToggle(self, 'Rooms', 'Logs')

        self.button_list = ButtonList(self)

        contain_list = QWidget()
        contain_list.setLayout(self.button_list)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setAlignment(Qt.AlignTop)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(contain_list)
        self.scroll.setMinimumHeight(self.height - (Style.unit / 4))

        self.addWidget(self.list_toggle)
        self.addWidget(self.scroll)
        self.addStretch(2)

    def add_button(self, label):
        self.button_list.add_button(label)
###############################


###############################
# VIEW PANEL CONTAINER
#   - Header Block [CONTAINER]
#   - Stream Grid [CONTAINER]
class ViewPanelContainer(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(ViewPanelContainer, self).__init__(ascendent=ascendent)
        self.set_dimensions((self.width / 5) * 4, self.height)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        self.header = ViewHeaderContainer(self)
        self.grid = ViewGridContainer(self)

        # Dark Header
        contain_header = QWidget()
        contain_header.setLayout(self.header)
        contain_header.setStyleSheet(Style.replace_variables('border: @BorderThick solid black;'))
        contain_header.setStyleSheet(Style.light)
        contain_header.setMinimumWidth(self.width)
        contain_header.setMinimumHeight(int(self.header.height))

        line = QHSeperationLine()
        line.setStyleSheet(Style.replace_variables('background-color: black;'))

        self.addWidget(contain_header, 4)
        self.addWidget(line)
        self.addLayout(self.grid, 22)
# VIEW HEADER CONTAINER
#   - Watchdog Logo [WIDGET]
#   - Watchdog Text [WIDGET]
#   - User Icon [WIDGET]
class ViewHeaderContainer(QHBoxLayout, Component):
    def __init__(self, ascendent):
        super(ViewHeaderContainer, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height / 26) * 4)
        self.setContentsMargins(0, 0, 0, 0)

        self.icon_logo = QLabel()
        self.icon_header = QLabel()
        self.btn_user = QPushButton()

        map_logo = QPixmap('assets/icons/watchdog.png')
        self.icon_logo.setPixmap(map_logo.scaled(Style.sizes.icon_logo, Style.sizes.icon_logo, Qt.KeepAspectRatio, Qt.FastTransformation))

        self.lbl_header = QLabel()
        self.lbl_header.setText('WATCHDOG')
        self.lbl_header.setStyleSheet(Style.replace_variables('font: @HeadTextSize @TextFont; \
                                                                font-weight: 50;'))

        map_user = QPixmap('assets/icons/user.png')
        self.btn_user.setIcon(QIcon(map_user))
        self.btn_user.setIconSize(QSize(Style.sizes.icon_large, Style.sizes.icon_large))

        self.icon_logo.setContentsMargins(int(Style.unit / 8), 0, int(Style.unit / 16), 0)
        self.btn_user.setContentsMargins(0, 0, int(Style.unit / 8), 0)

        self.addWidget(self.icon_logo)
        self.addWidget(self.lbl_header, Qt.AlignLeft)
        self.addStretch(6)
        self.addWidget(self.btn_user, Qt.AlignRight)
# VIEW GRID CONTAINER
#   - Stream Views [WIDGET]
class ViewGridContainer(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(ViewGridContainer, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 5)
        self.setSpacing(0)
        self.setAlignment(Qt.AlignTop)

        spacer = QSpacerItem(self.width, int(Style.unit / 8), QSizePolicy.Fixed)
        self.view_toggle = CenterToggle(self, 'Live', 'Clips')

        layout_above = QVBoxLayout()
        layout_above.setAlignment(Qt.AlignCenter)
        layout_above.addSpacerItem(spacer)
        layout_above.addWidget(self.view_toggle)

        self.viewer = StreamGrid(self)

        center_viewer = QVBoxLayout()
        center_viewer.setAlignment(Qt.AlignLeft)
        center_viewer.addLayout(self.viewer)
        center_viewer.addStretch()
        # Widget that contains the collection of Vertical Box
        self.contain_viewer = QWidget()
        self.contain_viewer.setLayout(center_viewer)
        self.contain_viewer.setStyleSheet(Style.replace_variables('border: @None; \
                                                            background-color: @LightColor;'))

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.contain_viewer)
        self.scroll.setMinimumWidth(self.width)
        self.scroll.setStyleSheet(Style.replace_variables('margin: ' + str(Style.unit / 8) + 'px; \
                                                            padding: ' + str(Style.unit / 8) + 'px; \
                                                            border: @BorderThin solid @LightTextColor; \
                                                            border-radius: @LargeRadius; \
                                                            background-color: @LightColor;'))

        self.addLayout(layout_above)
        self.addWidget(self.scroll)

    def set_stream_views(self, cameras):
        self.viewer.clear_views()
        self.viewer.add_views(cameras)

    def add_stream_view(self, camera):
        self.viewer.add_view(camera)
###############################
