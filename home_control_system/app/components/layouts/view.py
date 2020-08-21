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
    QSpacerItem,
    QSizePolicy,
    QScrollArea
)
from ..style import Style
from ..component import Component
from ..widgets.containers import StreamGrid
from ..widgets.spacers import QHSeperationLine
from ..popups import LoginPopup
from ..widgets.buttons import (
    PopupButton,
    CenterToggle
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
class HeaderLayout(QHBoxLayout, Component):
    def __init__(self, ascendent):
        super(HeaderLayout, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height / 26) * 4)
        self.setContentsMargins(0, 0, 0, 0)

        self.icon_logo = QLabel()
        self.icon_header = QLabel()
        # self.btn_user = QPushButton()
        self.btn_user = PopupButton(self, LoginPopup)

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
class GridLayout(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(GridLayout, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 5)
        self.setSpacing(0)
        self.setAlignment(Qt.AlignTop)

        spacer = QSpacerItem(self.width, int(Style.unit / 8), QSizePolicy.Fixed)
        self.view_toggle = CenterToggle(self, 'Live', 'Clips')
        layout_above = QVBoxLayout()
        layout_above.setAlignment(Qt.AlignCenter)
        layout_above.addSpacerItem(spacer)
        layout_above.addWidget(self.view_toggle)

        # Live Viewer
        self.viewer = StreamGrid(self)
        # Historical Viewer
        self.retriever = StreamGrid(self)

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

        contain_both = QVBoxLayout()
        contain_both.addWidget(self.live_viewer)
        contain_both.addWidget(self.historical_viewer)
        self.live_view = False
        self.toggle()

        # Widget that contains the collection of Vertical Box
        self.contain_viewer = QWidget()
        self.contain_viewer.setLayout(contain_both)
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