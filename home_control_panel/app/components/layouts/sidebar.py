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
    QScrollArea
)
from ..component import Component
from ..style import Style
from ..widgets.containers import ButtonList
from ..popups import SettingsPopup
<<<<<<< Updated upstream
from ..widgets.buttons import (
    PanelToggle,
    PopupButton
)
from ..widgets.spacers import (
    QHSeperationLine,
    QVSeperationLine
)
=======
from ..widgets.buttons import PopupButton
>>>>>>> Stashed changes

###############################
# SIDE PANEL CONTAINER
#   - Side Header Container [CONTAINER]
#   - List Toggle [CONTAINER]
class SideBar(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(SideBar, self).__init__(ascendent=ascendent)
<<<<<<< Updated upstream
        self.set_dimensions(self.width / 5, self.height)
=======
        self.set_dimensions(self.width * 1/5, self.height)
>>>>>>> Stashed changes
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
        self.setAlignment(Qt.AlignLeft)

        self.header = SettingLayout(self)
        self.list = ToggleLayout(self)

<<<<<<< Updated upstream
        # Dark Header
        contain_location = QWidget()
        contain_location.setLayout(self.header)
        contain_location.setStyleSheet(Style.light)
        contain_location.setStyleSheet(Style.replace_variables('background-color: @AltDarkColor;'))
        contain_location.setMinimumHeight(int(self.header.height))
        # contain_location.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))

        contain_list = QWidget()
        contain_list.setLayout(self.list)
        contain_list.setStyleSheet(Style.light)
        contain_list.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=6, xOffset=3, yOffset=3))

        line_h = QHSeperationLine()
        line_h.setStyleSheet(Style.replace_variables('background-color:black;'))

        line_v = QVSeperationLine()
        line_v.setStyleSheet(Style.replace_variables('background-color:black;'))

        line_alt = QVSeperationLine()
        line_alt.setStyleSheet(Style.replace_variables('background-color:white;'))

        holder_layout_top = QHBoxLayout()
        holder_layout_top.addWidget(contain_location)
        # holder_layout_top.addWidget(line_v)

        holder_layout_bottom = QHBoxLayout()
        holder_layout_bottom.addWidget(contain_list)
        # holder_layout_bottom.addWidget(line_alt)

        self.addLayout(holder_layout_top, 4)
        # self.addWidget(line_h)
        self.addLayout(holder_layout_bottom, 22)
=======
        contain_list = QWidget()
        contain_list.setLayout(self.list)
        contain_list.setStyleSheet(Style.light)

        self.addWidget(self.header)
        self.addWidget(contain_list)
>>>>>>> Stashed changes
# SIDE HEADER CONTAINER
#   - Home Icon [WIDGET]
#   - Location Label [WIDGET]
#   - Settings Button [WIDGET]
class SettingLayout(QWidget, Component):
    def __init__(self, ascendent):
<<<<<<< Updated upstream
        super(HeaderLayout, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height / 26) * 4)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
        self.setAlignment(Qt.AlignLeft)
=======
        super(SettingLayout, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height * 0.12))
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(self.height)
>>>>>>> Stashed changes

        self.icon_home = QLabel()
        self.lbl_location = QLabel()
<<<<<<< Updated upstream
        self.btn_settings = PopupButton(self, SettingsPopup)

        map_home = QPixmap('assets/icons/home.png')
        self.icon_home.setPixmap(map_home.scaled(Style.sizes.icon_medium, Style.sizes.icon_medium, Qt.KeepAspectRatio, Qt.FastTransformation))
=======
>>>>>>> Stashed changes
        self.lbl_location.setText(Component.root.settings.settings['site'])
        self.lbl_location.setStyleSheet(Style.replace_variables('font: @SubTextSize @TextFont; \
                                                                color: @HighlightColor; \
                                                                font-weight: 30;'))
        map_settings = QPixmap('assets/icons/settings.png')
        self.btn_settings = PopupButton(self, SettingsPopup)
        self.btn_settings.setIcon(QIcon(map_settings))
        self.btn_settings.setIconSize(QSize(Style.sizes.icon_medium, Style.sizes.icon_medium))

<<<<<<< Updated upstream
        self.icon_home.setContentsMargins(int(Style.unit / 8), 0, int(Style.unit / 24), 0)
        self.btn_settings.setContentsMargins(0, 0, int(Style.unit / 8), 0)

        self.addWidget(self.icon_home)
        self.addWidget(self.lbl_location)
        self.addStretch(1)
        self.addWidget(self.btn_settings, Qt.AlignRight)

        # self.btn_settings.clicked.connect(show_popup())
=======
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.lbl_location)
        layout.addStretch()

        style_widget = QWidget()
        style_widget.setLayout(layout)
        style_widget.setStyleSheet(Style.replace_variables('border-radius: @LargeRadius; \
                                                            margin: @MediumMargin; \
                                                            padding: @SmallPadding;'))
        head = QHBoxLayout()
        head.addWidget(style_widget)
        self.setLayout(layout)
>>>>>>> Stashed changes
# SIDE LIST TOGGLE CONTAINER
#   - Button Toggle [WIDGET]
#   - Button List [WIDGET]
class ToggleLayout(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(ToggleLayout, self).__init__(ascendent=ascendent)
<<<<<<< Updated upstream
        self.set_dimensions(self.width, (self.height / 26) * 23)
=======
        self.set_dimensions(self.width, (self.height * 0.88))
>>>>>>> Stashed changes
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
        self.setAlignment(Qt.AlignCenter)

        self.button_list = ButtonList(self)

        self.location_list = QWidget()
        self.location_list.setLayout(self.button_list)
        self.location_list.setMaximumWidth(self.width)

        list_container = QHBoxLayout()
        list_container.addStretch()
        list_container.addWidget(self.location_list)
        list_container.addStretch()

        container_widget = QWidget()
        container_widget.setLayout(list_container)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setAlignment(Qt.AlignTop)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(container_widget)
        self.scroll.setMinimumHeight(self.height - (Style.unit / 4))

        self.addStretch()
        self.addWidget(self.scroll)
        self.addStretch(2)

    def show(self):
        self.location_list.show()
        self.update()

    def hide(self):
        self.location_list.hide()

    def toggle(self):
        self.update()

    def add_button(self, label):
        self.button_list.add_button(label)

    def clear(self):
        self.button_list.clear_buttons()
###############################
