import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QPixmap,
    QIcon
)
from PyQt5.QtWidgets import (
    QWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QScrollArea,
    QLabel
)
from .widgets import (
    StreamView,
    StreamGrid,
    ButtonToggle
)
from .component import Component
from .styles import style_dark

# setContentsMargins(left, top, right, bottom)


###############################
# MAIN WINDOW
class Window(QMainWindow, Component):
    def __init__(self, ascendent=None):
        super(Window, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)

        (width, height) = self.ascendent.get_resolution()
        Component.unit = (width / 2) / 5  # 1 Component.unit = (1/2 width) / 5 segments
        self.set_dimensions(5 * Component.unit, 3 * Component.unit)

        self.setWindowTitle("Home Control Panel")
        self.setContentsMargins(0, 0, 0, 0)
        self.setGeometry(int(self.width / 2), int(self.height / 2), self.width, self.height)

    def buildLayout(self, cameras):
        home = HomeContainer(self)
        home.add_cameras(cameras)

        spacer = QSpacerItem(self.width, int(Component.unit / 8), QSizePolicy.Fixed)
        layout = QVBoxLayout()
        layout.addSpacerItem(spacer)
        layout.addLayout(home)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        contain_layout = QWidget()
        contain_layout.setLayout(layout)

        self.setCentralWidget(contain_layout)

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
        self.view = ViewPanelContainer(self)

        self.addLayout(self.sidepanel, 1)
        self.addLayout(self.view, 4)

    def add_cameras(self, cameras):
        self.view.stream_grid.set_stream_views(cameras)
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

        self.location = SideHeaderContainer(self)
        self.room_list = SideListToggleContainer(self)

        # Dark Header
        contain_location = QWidget()
        contain_location.setLayout(self.location)
        contain_location.setStyleSheet(style_dark)

        self.addWidget(contain_location, 3)
        self.addLayout(self.room_list, 23)
# SIDE HEADER CONTAINER
#   - Home Icon [WIDGET]
#   - Location Label [WIDGET]
#   - Settings Button [WIDGET]
class SideHeaderContainer(QHBoxLayout, Component):
    def __init__(self, ascendent):
        super(SideHeaderContainer, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height / 26) * 3)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        self.lbl_location = QLabel()
        self.icon_home = QLabel()
        self.btn_settings = QPushButton()

        map = QPixmap("assets/icons/home.png")
        self.icon_home.setPixmap(map.scaled(int(Component.unit / 8), int(Component.unit / 8), Qt.KeepAspectRatio, Qt.FastTransformation))

        self.lbl_location.setText("Home")

        map = QPixmap("assets/icons/settings.png")
        self.btn_settings.setIcon(QIcon(map.scaled(int(Component.unit / 4), int(Component.unit / 4), Qt.KeepAspectRatio, Qt.FastTransformation)))

        self.icon_home.setContentsMargins(int(Component.unit / 8), 0, int(Component.unit / 24), 0)
        self.btn_settings.setContentsMargins(0, 0, int(Component.unit / 8), 0)

        self.addWidget(self.icon_home)
        self.addWidget(self.lbl_location)
        self.addStretch(1)
        self.addWidget(self.btn_settings, Qt.AlignRight)
# SIDE LIST TOGGLE CONTAINER
#   - Button Toggle [WIDGET]
#   - Button List [WIDGET]
class SideListToggleContainer(QHBoxLayout, Component):
    def __init__(self, ascendent):
        super(SideListToggleContainer, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height / 26) * 23)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
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
        self.stream_grid = ViewGridContainer(self)

        # Dark Header
        contain_header = QWidget()
        contain_header.setLayout(self.header)
        contain_header.setStyleSheet(style_dark)

        self.addWidget(contain_header, 3)
        self.addLayout(self.stream_grid, 23)
# VIEW HEADER CONTAINER
#   - Watchdog Logo [WIDGET]
#   - Watchdog Text [WIDGET]
#   - User Icon [WIDGET]
class ViewHeaderContainer(QHBoxLayout, Component):
    def __init__(self, ascendent):
        super(ViewHeaderContainer, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height / 26) * 3)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        self.icon_logo = QLabel()
        self.icon_header = QLabel()
        self.btn_user = QPushButton()

        map = QPixmap("assets/icons/watchdog.png")
        self.icon_logo.setPixmap(map.scaled(110, 110, Qt.KeepAspectRatio, Qt.FastTransformation))

        map = QPixmap("assets/icons/header.png")
        self.icon_header.setPixmap(map.scaledToHeight(45))

        map = QPixmap("assets/icons/user.png")
        self.btn_user.setIcon(QIcon(map.scaled(int(Component.unit / 2), int(Component.unit / 2), Qt.KeepAspectRatio, Qt.FastTransformation)))
        
        self.icon_logo.setContentsMargins(int(Component.unit / 8), 0, int(Component.unit / 16), 0)
        self.btn_user.setContentsMargins(0, 0, int(Component.unit / 8), 0)

        self.addWidget(self.icon_logo)
        self.addWidget(self.icon_header, Qt.AlignLeft)
        self.addStretch(1)
        self.addWidget(self.btn_user, Qt.AlignRight)
# VIEW GRID CONTAINER
#   - Stream Views [WIDGET]
class ViewGridContainer(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(ViewGridContainer, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        self.view_toggle = ButtonToggle()

        self.viewer = StreamGrid(self)

        contain_viewer = QWidget()                 # Widget that contains the collection of Vertical Box
        contain_viewer.setLayout(self.viewer)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(contain_viewer)

        self.view_toggle.setContentsMargins(0, int(Component.unit / 4), 0, int(Component.unit / 4))

        self.addLayout(self.view_toggle)
        self.addWidget(self.scroll)

    def set_stream_views(self, cameras):
        views = []
        for index in range(len(cameras)):
            view = StreamView()
            cameras[index].stream.add_stream_view(view, (Component.unit, Component.unit * 0.6))
            views.append(view)
        self.viewer.set_views(views)
###############################
