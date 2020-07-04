import sys
from PyQt5.QtCore import (
    Qt,
    QSize
)
from PyQt5.QtGui import (
    QPixmap,
    QIcon
)
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
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
    StreamView,
    StreamGrid,
    ButtonToggle,
    ButtonList,
    QVSeperationLine,
    QHSeperationLine
)
from .component import Component
from .styles import style_dark


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

        home_container = QWidget()
        home_container.setMinimumWidth(self.width)
        home_container.setLayout(home)

        spacer = QSpacerItem(self.width, int(Component.unit / 16), QSizePolicy.Fixed)
        line = QHSeperationLine()
        line.setStyleSheet("background-color:black;")

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
        line.setStyleSheet("background-color:black;")

        self.addWidget(contain_panel, 1)
        self.addWidget(line)
        self.addWidget(contain_view, 4)

    def add_cameras(self, cameras):
        self.view.grid.set_stream_views(cameras)
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
        contain_location.setStyleSheet(style_dark)
        contain_location.setMinimumHeight(int(self.header.height))

        shadow = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        contain_location.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))

        line_h = QHSeperationLine()
        line_h.setStyleSheet("background-color:black;")

        line_v = QVSeperationLine()
        line_v.setStyleSheet("background-color:black;")

        line_alt = QVSeperationLine()
        line_alt.setStyleSheet("background-color:white;")

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
        self.btn_settings = QPushButton()

        map_home = QPixmap("assets/icons/home.png")
        self.icon_home.setPixmap(map_home.scaled(int(Component.unit / 8), int(Component.unit / 8), Qt.KeepAspectRatio, Qt.FastTransformation))
        self.lbl_location.setText("Home")
        map_settings = QPixmap("assets/icons/settings.png")
        self.btn_settings.setIcon(QIcon(map_settings))
        self.btn_settings.setIconSize(QSize(int(Component.unit / 8), int(Component.unit / 8)))

        self.icon_home.setContentsMargins(int(Component.unit / 8), 0, int(Component.unit / 24), 0)
        self.btn_settings.setContentsMargins(0, 0, int(Component.unit / 8), 0)

        self.addWidget(self.icon_home)
        self.addWidget(self.lbl_location)
        self.addStretch(1)
        self.addWidget(self.btn_settings, Qt.AlignRight)
# SIDE LIST TOGGLE CONTAINER
#   - Button Toggle [WIDGET]
#   - Button List [WIDGET]
class SideListToggleContainer(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(SideListToggleContainer, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height / 26) * 23)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        self.list_toggle = ButtonToggle(self, 'Rooms', 'Logs')

        contain_toggle = QWidget()
        contain_toggle.setLayout(self.list_toggle)
        contain_toggle.setStyleSheet('background-color: #1d2125;')

        shadow = QGraphicsDropShadowEffect(blurRadius=3, xOffset=2, yOffset=3)
        contain_toggle.setGraphicsEffect(shadow)

        self.button_list = ButtonList(self)
        self.button_list.addButton('Living Room')
        self.button_list.addButton('Kitchen')
        self.button_list.addButton('Master Bedroom')
        self.button_list.addButton('Kids Room')
        self.button_list.addButton('Kids Room')
        self.button_list.addButton('Kids Room')

        contain_list = QWidget()
        contain_list.setLayout(self.button_list)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setAlignment(Qt.AlignTop)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(contain_list)
        self.scroll.setMinimumHeight(self.height - (Component.unit / 4))

        self.addWidget(contain_toggle)
        self.addWidget(self.scroll)
        self.addStretch(2)
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
        contain_header.setStyleSheet("border: 2px solid black;")
        contain_header.setStyleSheet(style_dark)
        contain_header.setMinimumWidth(self.width)
        contain_header.setMinimumHeight(int(self.header.height))

        line = QHSeperationLine()
        line.setStyleSheet("background-color:black;")

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

        map_logo = QPixmap("assets/icons/watchdog.png")
        self.icon_logo.setPixmap(map_logo.scaled(int(Component.unit * 0.33), int(Component.unit * 0.33), Qt.KeepAspectRatio, Qt.FastTransformation))

        self.lbl_header = QLabel()
        self.lbl_header.setText("WATCHDOG")
        self.lbl_header.setStyleSheet("font: 60px Corbel, sans-serif; font-weight: 50;")

        map_user = QPixmap("assets/icons/user.png")
        self.btn_user.setIcon(QIcon(map_user))
        self.btn_user.setIconSize(QSize(int(Component.unit / 4), int(Component.unit / 4)))

        self.icon_logo.setContentsMargins(int(Component.unit / 8), 0, int(Component.unit / 16), 0)
        self.btn_user.setContentsMargins(0, 0, int(Component.unit / 8), 0)

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
        self.setAlignment(Qt.AlignCenter)

        self.view_toggle = ButtonToggle(self, 'Live', 'History')
        self.view_toggle.contain_toggle.setStyleSheet("background-color: #1d2125; border-radius: 20px;") 

        toggle_layout = QHBoxLayout()
        toggle_layout.setAlignment(Qt.AlignCenter)
        toggle_layout.addLayout(self.view_toggle)

        contain_layout = QWidget()
        # contain_layout.setMaximumWidth(self.width)
        contain_layout.setFixedHeight(Component.unit / 2)
        contain_layout.setLayout(toggle_layout)

        layout_above = QVBoxLayout()
        layout_above.setAlignment(Qt.AlignCenter)
        layout_above.addWidget(contain_layout)

        self.viewer = StreamGrid(self)

        contain_viewer = QWidget()                 # Widget that contains the collection of Vertical Box
        contain_viewer.setMinimumWidth(self.width)
        contain_viewer.setLayout(self.viewer)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(contain_viewer)
        self.scroll.setMaximumWidth(self.width)

        self.addLayout(layout_above)
        self.addWidget(self.scroll)

    def set_stream_views(self, cameras):
        views = []
        for index in range(len(cameras)):
            view = StreamView()
            cameras[index].stream.add_stream_view(view, (Component.unit, Component.unit * 0.6))
            views.append(view)
        self.viewer.set_views(views)
###############################
