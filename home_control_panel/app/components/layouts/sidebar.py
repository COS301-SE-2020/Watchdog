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
from ..widgets.buttons import PopupButton

###############################
# SIDE PANEL CONTAINER
#   - Side Header Container [CONTAINER]
#   - List Toggle [CONTAINER]
class SideBar(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(SideBar, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width * 1/5, self.height)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
        self.setAlignment(Qt.AlignLeft)

        self.header = SettingLayout(self)
        self.list = ToggleLayout(self)

        contain_list = QWidget()
        contain_list.setLayout(self.list)
        contain_list.setStyleSheet(Style.light)

        self.addWidget(self.header)
        self.addWidget(contain_list)
# SIDE HEADER CONTAINER
#   - Home Icon [WIDGET]
#   - Location Label [WIDGET]
#   - Settings Button [WIDGET]
class SettingLayout(QWidget, Component):
    def __init__(self, ascendent):
        super(SettingLayout, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height * 0.12))
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(self.height)

        self.lbl_location = QLabel()
        self.lbl_location.setText(Component.root.settings.settings['site'])
        self.lbl_location.setStyleSheet(Style.replace_variables('font: @SubTextSize @TextFont; \
                                                                color: @HighlightColor; \
                                                                font-weight: 30;'))
        map_settings = QPixmap('assets/icons/settings.png')
        self.btn_settings = PopupButton(self, SettingsPopup)
        self.btn_settings.setIcon(QIcon(map_settings))
        self.btn_settings.setIconSize(QSize(Style.sizes.icon_medium, Style.sizes.icon_medium))

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
# SIDE LIST TOGGLE CONTAINER
#   - Button Toggle [WIDGET]
#   - Button List [WIDGET]
class ToggleLayout(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(ToggleLayout, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height * 0.88))
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
