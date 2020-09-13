from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QScrollArea,
    QGraphicsDropShadowEffect
)
from ..style import Style
from ..component import Component
<<<<<<< Updated upstream
from ..widgets.spacers import QHSeperationLine
from ..popups import LoginPopup, LoginContainer
from ..widgets.buttons import (
    PopupButton,
    CenterToggle
)
=======
from ..widgets.buttons import CenterToggle
>>>>>>> Stashed changes
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
        self.set_dimensions(self.width * 4/5, self.height * 1/8)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        self.grid = GridLayout(self)

        # # Light View
        contain_grid = QWidget()
        contain_grid.setContentsMargins(0, 0, 0, 0)
        contain_grid.setLayout(self.grid)
        contain_grid.setStyleSheet(Style.light)
        contain_grid.setMinimumWidth(self.width)
<<<<<<< Updated upstream
        contain_grid.setMinimumHeight(int(self.header.height))

        line = QHSeperationLine()
        line.setStyleSheet(Style.replace_variables('background-color: black;'))

        self.addWidget(contain_header, 4)
        # self.addWidget(line)
        self.addWidget(contain_grid, 22)
# VIEW HEADER CONTAINER
#   - Watchdog Logo [WIDGET]
#   - Watchdog Text [WIDGET]
#   - User Icon [WIDGET]
class HeaderLayout(QHBoxLayout, Component):
    def __init__(self, ascendent):
        super(HeaderLayout, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height / 26) * 4)
        self.setContentsMargins(0, 0, 0, 0)

        self.icon_logo = QLabel()
        self.icon_header = QLabel()

        self.btn_user = QPushButton()
        self.btn_user.clicked.connect(self.toggle_login)
        
        map_logo = QPixmap('assets/icons/watchdog.png')
        self.icon_logo.setPixmap(map_logo.scaled(Style.sizes.icon_logo, Style.sizes.icon_logo, Qt.KeepAspectRatio, Qt.FastTransformation))

        self.lbl_header = QLabel()
        self.lbl_header.setText('CONTROL PANEL')
        self.lbl_header.setStyleSheet(Style.replace_variables('font: @HeadTextSize @TextFont; \
                                                                font-weight: 50;'))

        map_user = QPixmap('assets/icons/user.png')
        self.btn_user.setIcon(QIcon(map_user))
        self.btn_user.setIconSize(QSize(Style.sizes.icon_large, Style.sizes.icon_large))

        self.icon_logo.setContentsMargins(int(Style.unit / 8), 0, int(Style.unit / 24), 0)

        self.login_shown = False
        self.login = LoginContainer(self)

        self.addWidget(self.icon_logo)
        self.addWidget(self.lbl_header, Qt.AlignLeft)
        self.addStretch(15)
        self.addWidget(self.btn_user, Qt.AlignRight)
        self.addWidget(self.login, Qt.AlignRight)

    def toggle_login(self):
        if self.login_shown:
            self.login_shown = False
            self.login.submit()
        else:
            self.login_shown = True
            self.login.show()
=======
>>>>>>> Stashed changes

        self.addWidget(contain_grid)
# VIEW GRID CONTAINER
#   - Stream Views [WIDGET]
class GridLayout(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(GridLayout, self).__init__(ascendent=ascendent)
<<<<<<< Updated upstream
        self.setContentsMargins(0, 0, 0, 5)
=======
        self.set_dimensions(self.width, self.height * 7/8)
        self.setContentsMargins(0, 0, 0, 0)
>>>>>>> Stashed changes
        self.setSpacing(0)
        self.setAlignment(Qt.AlignCenter)

        spacer = QSpacerItem(self.width, int(Style.unit / 8), QSizePolicy.Fixed)
        self.view_toggle = CenterToggle(self, 'Live', 'Clips')
        layout_above = QVBoxLayout()
        layout_above.setAlignment(Qt.AlignCenter)
<<<<<<< Updated upstream
        layout_above.addSpacerItem(spacer)
        layout_above.addWidget(self.view_toggle)

        # Live Viewer
=======
        layout_above.setContentsMargins(0, 0, 0, 0)
        layout_above.setSpacing(0)
        layout_above.addStretch(12)
        layout_above.addWidget(self.view_toggle)

        widget_above = QWidget()
        widget_above.setLayout(layout_above)
        widget_above.setContentsMargins(0, 0, 0, 0)
        widget_above.setFixedHeight(Style.unit * 0.32)

>>>>>>> Stashed changes
        self.viewer = StreamGrid(self)
        # Historical Viewer
        self.retriever = VideoGrid(self)

        contain_live = QVBoxLayout()
        contain_live.setAlignment(Qt.AlignLeft)
        contain_live.addLayout(self.viewer)
        contain_live.addStretch()

        contain_historical = QVBoxLayout()
        contain_historical.setAlignment(Qt.AlignLeft)
        contain_historical.addLayout(self.retriever)
        contain_historical.addStretch()

        self.live_viewer = QWidget()
        self.live_viewer.setLayout(contain_live)

        self.historical_viewer = QWidget()
        self.historical_viewer.setLayout(contain_historical)

        self.info_label = QWidget()
        info_box = QHBoxLayout()
        info_box.setAlignment(Qt.AlignCenter)
        info_box.addWidget(QLabel('Login to view your content...'))
        self.info_label.setLayout(info_box)

<<<<<<< Updated upstream
        contain_both = QVBoxLayout()
=======
        contain_both = QHBoxLayout()
        contain_both.setContentsMargins(0, 0, 0, 0)

>>>>>>> Stashed changes
        contain_both.addWidget(self.live_viewer)
        contain_both.addWidget(self.historical_viewer)
        contain_both.addWidget(self.info_label)
        self.live_view = False
        self.toggle()

        # Widget that contains the collection of Vertical Box
        self.contain_viewer = QWidget()
        self.contain_viewer.setLayout(contain_both)
        self.contain_viewer.setStyleSheet(Style.replace_variables('border: @None; \
<<<<<<< Updated upstream
                                                            background-color: @DarkColor;'))
=======
                                                                margin @None; \
                                                                padding @None; \
                                                                background-color: @DarkColor;'))
>>>>>>> Stashed changes
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.contain_viewer)
        self.scroll.setMinimumWidth(self.width)
<<<<<<< Updated upstream
        self.scroll.setStyleSheet(Style.replace_variables('margin: ' + str(Style.unit / 8) + 'px; \
                                                            padding: ' + str(Style.unit / 8) + 'px; \
                                                            border: none; \
                                                            border-radius: @LargeRadius; \
                                                            background-color: @DarkColor;'))
        self.scroll.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=14, xOffset=2, yOffset=5))
        self.addLayout(layout_above)
        self.addWidget(self.scroll)
=======

        main_container = QVBoxLayout()
        main_container.setContentsMargins(0, 0, 0, 0)
        main_container.setAlignment(Qt.AlignCenter)
        main_container.addWidget(widget_above)
        main_container.addWidget(self.scroll)

        main_widget = QWidget()
        main_widget.setLayout(main_container)
        main_widget.setStyleSheet(Style.replace_variables('margin: ' + str(Style.sizes.margin_large * 1.4) + 'px; \
                                                            padding: @None; \
                                                            border: none; \
                                                            border-radius: @LargeRadius; \
                                                            background-color: @DarkColor;'))
        main_widget.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=10, xOffset=3, yOffset=3))

        self.addWidget(main_widget)
>>>>>>> Stashed changes
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