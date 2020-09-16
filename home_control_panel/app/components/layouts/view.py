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
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QPushButton,
    QGraphicsDropShadowEffect
)
from ..style import Style
from ..component import Component
from ..widgets.spacers import QHSeperationLine
# from ..popups import LoginContainer
from ..widgets.buttons import CenterToggle
from ..widgets.containers import (
    StreamGrid,
    VideoGrid
)

###############################
# VIEW PANEL CONTAINER
#   - Header Block [CONTAINER]
#   - Stream Grid [CONTAINER]
class View(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(View, self).__init__(ascendent=ascendent)
        self.set_dimensions((self.width / 5) * 4, self.height)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        self.header = HeaderLayout(self)
        self.grid = GridLayout(self)

        # Dark Header
        contain_header = QWidget()
        contain_header.setLayout(self.header)
        contain_header.setStyleSheet(Style.dark)
        contain_header.setStyleSheet(Style.replace_variables('background-color: @AltDarkColor;'))
        contain_header.setMinimumWidth(self.width)
        contain_header.setMinimumHeight(int(self.header.height))

        # Light View
        contain_grid = QWidget()
        contain_grid.setLayout(self.grid)
        contain_grid.setStyleSheet(Style.light)
        contain_grid.setMinimumWidth(self.width)
        contain_grid.setMinimumHeight(int(self.header.height))

        line_h = QHSeperationLine()
        line_h.setStyleSheet(Style.replace_variables('background-color:@LightColor; border: ' + str(Style.unit / 150) + 'px;'))

        self.addWidget(contain_header, 1)
        self.addWidget(line_h)
        self.addWidget(contain_grid, 9)
# VIEW HEADER CONTAINER
#   - Watchdog Logo [WIDGET]
#   - Watchdog Text [WIDGET]
#   - User Icon [WIDGET]
class HeaderLayout(QHBoxLayout, Component):
    def __init__(self, ascendent):
        super(HeaderLayout, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height * 0.1))
        self.setContentsMargins(0, 0, 0, 0)

        self.icon_logo = QLabel()
        self.icon_header = QLabel()

        self.btn_user = QPushButton()
        self.btn_user.clicked.connect(self.toggle_login)
        
        map_logo = QPixmap('assets/icons/icon.png')
        self.icon_logo.setFixedHeight(self.height)
        self.icon_logo.setPixmap(map_logo.scaled(Style.sizes.icon_logo, self.height * 0.8, Qt.KeepAspectRatio, Qt.FastTransformation))

        self.lbl_header = QLabel()
        self.lbl_header.setText('CONTROL PANEL')
        self.lbl_header.setStyleSheet(Style.replace_variables('font: @HeadTextSize @TextFont; \
                                                                font-weight: 50;'))

        map_user = QPixmap('assets/icons/user.png')
        self.btn_user.setIcon(QIcon(map_user))
        self.btn_user.setIconSize(QSize(Style.sizes.icon_large, Style.sizes.icon_large))
        self.btn_user.hide()

        self.icon_logo.setContentsMargins(int(Style.unit / 8), 0, int(Style.unit / 16), 0)

        self.addWidget(self.icon_logo)
        self.addWidget(self.lbl_header, Qt.AlignLeft)
        self.addStretch(15)
        self.addWidget(self.btn_user, Qt.AlignRight)

    def toggle_login(self):
        Component.root.login_screen.show()

# VIEW GRID CONTAINER
#   - Stream Views [WIDGET]
class GridLayout(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(GridLayout, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height * 0.9))
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
        self.setAlignment(Qt.AlignTop)

        self.view_toggle = CenterToggle(self, 'Live', 'Clips')

        layout_above = QVBoxLayout()
        layout_above.setAlignment(Qt.AlignBottom)
        layout_above.setContentsMargins(0, 0, 0, 0)

        layout_above.addStretch(2)
        layout_above.addWidget(self.view_toggle)

        widget_above = QWidget()
        widget_above.setLayout(layout_above)
        widget_above.setFixedHeight(Style.unit * 0.45)

        self.viewer = StreamGrid(self)
        self.retriever = VideoGrid(self)

        contain_live = QVBoxLayout()
        contain_live.setContentsMargins(0, 0, 0, 0)
        contain_live.setAlignment(Qt.AlignCenter)
        contain_live.addLayout(self.viewer)
        contain_live.addStretch()

        contain_historical = QVBoxLayout()
        contain_historical.setContentsMargins(0, 0, 0, 0)
        contain_historical.setAlignment(Qt.AlignCenter)
        contain_historical.addLayout(self.retriever)
        contain_historical.addStretch()

        self.live_viewer = QWidget()
        self.live_viewer.setLayout(contain_live)
        self.live_viewer.setFixedWidth(self.width * 0.85)

        self.historical_viewer = QWidget()
        self.historical_viewer.setLayout(contain_historical)
        self.historical_viewer.setFixedWidth(self.width * 0.85)

        info_box = QHBoxLayout()
        info_box.setAlignment(Qt.AlignCenter)
        info_box.addWidget(QLabel('Login to view your content...'))

        self.info_label = QWidget()
        self.info_label.setLayout(info_box)

        contain_both = QHBoxLayout()
        contain_both.addWidget(self.live_viewer)
        contain_both.addWidget(self.historical_viewer)
        contain_both.addWidget(self.info_label)

        self.live_view = False

        self.toggle()

        # Widget that contains the collection of Vertical Box
        self.contain_viewer = QWidget()
        self.contain_viewer.setContentsMargins(0, 0, 0, 0)
        self.contain_viewer.setLayout(contain_both)
        self.contain_viewer.setStyleSheet(Style.replace_variables('border: @None; \
                                                                   background-color: @DarkColor;'))
        self.scroll = QScrollArea()
        self.scroll.setContentsMargins(0, 0, 0, 0)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.contain_viewer)
        self.scroll.setMinimumWidth(self.width)

        main_container = QVBoxLayout()
        main_container.setAlignment(Qt.AlignTop)
        main_container.addWidget(widget_above)
        main_container.addWidget(self.scroll)

        main_widget = QWidget()
        main_widget.setLayout(main_container)
        main_widget.setStyleSheet(Style.replace_variables('margin: ' + str(Style.unit / 8) + 'px; \
                                                            padding: ' + str(Style.unit / 8) + 'px; \
                                                            border: none; \
                                                            border-radius: @LargeRadius; \
                                                            background-color: @DarkColor;'))
        main_widget.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=14, xOffset=2, yOffset=5))
        self.addWidget(main_widget)
        self.show()

    def show(self):
        self.info_label.hide()
        self.view_toggle.show()
        if self.live_view:
            self.live_viewer.show()
            self.historical_viewer.hide()
        else:
            self.historical_viewer.show()
            self.live_viewer.hide()
        self.update()

    def hide(self):
        self.info_label.show()
        self.view_toggle.hide()
        self.live_viewer.hide()
        self.historical_viewer.hide()

    def toggle(self):
        if self.live_view:
            self.live_view = False
            self.live_viewer.hide()
            self.historical_viewer.show()
        else:
            self.live_view = True
            self.historical_viewer.hide()
            self.live_viewer.show()
        self.update()

    def set_stream_views(self, cameras):
        self.viewer.reset(cameras)

    def add_stream_view(self, camera):
        self.viewer.add_view(camera)
###############################
