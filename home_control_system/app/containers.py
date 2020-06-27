import sys
from enum import Enum
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QPixmap, QIcon)
from PyQt5.QtWidgets import (
    QWidget,
    QMainWindow,
    QDesktopWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QScrollArea,
    QLabel
)
from .component import Component
from .widgets import StreamView

# Window Ratio: (5:3)
# unit = monitor_height / 2 / 3

unit = 1

class ComponentClass(Enum):
    WIDGET = 0
    SPACER = 1
    CONTAINER = 2

class Container(Component):
    def __init__(self, ascendent):
        super(Container, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)

    # Add Widgets / Layouts / Spaces
    def add(self, **kwargs):
        for key, value in kwargs.items():
            if key == ComponentClass.WIDGET:
                self.addWidget(value)
            elif key == ComponentClass.SPACER:
                self.addSpacerItem(value)
            elif key == ComponentClass.CONTAINER:
                self.addLayout(value)
###############################
# MAIN WINDOW
class Window(QMainWindow, Component):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Home Control Panel")
        unit = QDesktopWidget().screenGeometry(-1).height() / 2 / 3
        self.set_dimensions(5 * unit, 3 * unit)
        self.setGeometry(self.width / 2, self.height / 2, self.width, self.height)

    def buildLayout(self, cameras):
        layout = HomeContainer(self)
        layout.add_cameras(cameras)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def closeEvent(self, event):
        event.accept()  # let the window close
        sys.exit()

###############################


###############################
# MAIN LAYOUT CONTAINER
#   - Side Panel
#   - View Panel
class HomeContainer(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(HomeContainer, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)

        space_size = unit / 9
        self.set_dimensions(self.width, self.height - space_size)

        layout = QHBoxLayout()

        self.sidepanel = SideTabContainer(self)
        self.view = ViewContainer(self)

        layout.addLayout(self.sidepanel, 1)
        layout.addLayout(self.view, 4)

        spacer = QSpacerItem(self.width, space_size, QSizePolicy.Fixed)

        self.addSpacerItem(spacer)
        self.addLayout(layout)

    def add_cameras(self, cameras):
        self.view.stream_grid.set_stream_views(cameras)
###############################


###############################
# SIDE PANEL CONTAINER
#   - LocationContainer
#   - Rooms/Alerts List
class SideTabContainer(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(SideTabContainer, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width / 5, self.height)
        self.setContentsMargins(0, 0, 0, 0)

        self.location = LocationContainer(self)
        self.room_list = ListContainer(self)

        widget = QWidget()
        widget.setLayout(self.location)
        widget.setStyleSheet("background-color:#1d2125;")

        self.addWidget(widget, 3)
        self.addLayout(self.room_list, 23)


class LocationContainer(QHBoxLayout, Component):
    def __init__(self, ascendent):
        super(LocationContainer, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height / 26) * 3)
        self.setContentsMargins(0, 0, 0, 0)

        self.lbl_location = QLabel()
        self.icon_home = QLabel()
        self.btn_settings = QPushButton()

        # self.lbl_location.setAlignment(Qt.AlignLeft)
        # self.icon_home.setAlignment(Qt.AlignLeft)

        self.lbl_location.setText("Home")

        map = QPixmap("assets/icons/home.png")
        self.icon_home.setPixmap(map.scaled(50, 50, Qt.KeepAspectRatio, Qt.FastTransformation))

        map = QPixmap("assets/icons/settings.png")
        self.btn_settings.setIcon(QIcon(map.scaled(50, 50, Qt.KeepAspectRatio, Qt.FastTransformation)))

        self.addWidget(self.icon_home)
        self.addWidget(self.lbl_location)
        self.addWidget(self.btn_settings)


class ListContainer(QHBoxLayout, Component):
    def __init__(self, ascendent):
        super(ListContainer, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height / 26) * 23)
        self.setContentsMargins(0, 0, 0, 0)
###############################


###############################
# VIEW PANEL CONTAINER
#   - Header Block
#   - Stream Grid
class ViewContainer(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(ViewContainer, self).__init__(ascendent=ascendent)
        self.set_dimensions((self.width / 5) * 4, self.height)
        self.setContentsMargins(0, 0, 0, 0)

        self.header = HeaderContainer(self)

        self.header.setAlignment(Qt.AlignLeft)

        self.stream_grid = GridContainer(self)

        widget = QWidget()
        widget.setLayout(self.header)
        widget.setStyleSheet("background-color:#1d2125;")

        self.addWidget(widget, 3)
        self.addLayout(self.stream_grid, 23)


class HeaderContainer(QHBoxLayout, Component):
    def __init__(self, ascendent):
        super(HeaderContainer, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height / 26) * 3)
        self.setContentsMargins(0, 0, 0, 0)

        self.icon_logo = QLabel()
        self.icon_header = QLabel()
        self.btn_user = QPushButton()

        map = QPixmap("assets/icons/watchdog.png")
        self.icon_logo.setPixmap(map.scaled(110, 110, Qt.KeepAspectRatio, Qt.FastTransformation))
        self.icon_logo.setContentsMargins(unit / 2, unit / 2, unit / 4, unit / 2)
        map = QPixmap("assets/icons/header.png")
        self.icon_header.setPixmap(map.scaledToHeight(45))
        self.icon_logo.setContentsMargins(unit / 2, unit / 2, unit / 2, unit / 2)
        map = QPixmap("assets/icons/user.png")
        self.btn_user.setIcon(QIcon(map.scaled(50, 50, Qt.KeepAspectRatio, Qt.FastTransformation)))

        self.addWidget(self.icon_logo)
        self.addWidget(self.icon_header)
        self.addWidget(self.btn_user)


class GridContainer(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(GridContainer, self).__init__(ascendent=ascendent)
        self.setContentsMargins(unit, unit, unit, unit)

        self.viewer = StreamGrid(self)

        widget = QWidget()                 # Widget that contains the collection of Vertical Box
        widget.setLayout(self.viewer)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(widget)

        self.addWidget(self.scroll)

    def set_stream_views(self, cameras):
        views = []
        for index in range(len(cameras)):
            view = StreamView()
            cameras[index].init_stream(view, self.width / 3, self.width / 4.8)
            views.append(view)
        self.viewer.set_views(views)

class StreamGrid(QGridLayout, Component):
    def __init__(self, ascendent):
        super(StreamGrid, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height / 26) * 23)
        self.setContentsMargins(unit / 4, unit / 4, unit / 4, unit / 4)

    def set_views(self, views):
        (row, col) = (0, 0)
        for index in range(len(views)):
            if col > 2:
                row += 1
                col = 0
            self.addWidget(views[index], row, col)
            col += 1
###############################
