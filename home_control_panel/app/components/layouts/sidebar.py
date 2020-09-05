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
    QGraphicsDropShadowEffect
)
from ..component import Component
from ..style import Style
from ..widgets.containers import (
    ButtonList,
    LabelList
)
from ..popups import SettingsPopup
from ..widgets.buttons import (
    PanelToggle,
    PopupButton
)
from ..widgets.spacers import (
    QHSeperationLine
)

###############################
# SIDE PANEL CONTAINER
#   - Side Header Container [CONTAINER]
#   - List Toggle [CONTAINER]
class SideBar(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(SideBar, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width / 6, self.height)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
        self.setAlignment(Qt.AlignLeft)

        self.header = HeaderLayout(self)
        self.list = ToggleLayout(self)

        # Dark Header
        contain_location = QWidget()
        contain_location.setLayout(self.header)
        contain_location.setStyleSheet(Style.light)
        contain_location.setStyleSheet(Style.replace_variables('background-color: @AltDarkColor;'))
        contain_location.setMinimumHeight(int(self.header.height))

        contain_list = QWidget()
        contain_list.setLayout(self.list)
        contain_list.setStyleSheet(Style.light)
        contain_list.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=6, xOffset=3, yOffset=3))

        line_h = QHSeperationLine()
        line_h.setStyleSheet(Style.replace_variables('background-color:@LightColor; border: ' + str(Style.unit / 150) + 'px;'))

        holder_layout_top = QHBoxLayout()
        holder_layout_top.addWidget(contain_location)
        contain_location.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))

        holder_layout_bottom = QHBoxLayout()
        holder_layout_bottom.addWidget(contain_list)

        self.addWidget(contain_location, 4)
        self.addWidget(line_h)
        self.addWidget(contain_list, 22)
# SIDE HEADER CONTAINER
#   - Home Icon [WIDGET]
#   - Location Label [WIDGET]
#   - Settings Button [WIDGET]
class HeaderLayout(QHBoxLayout, Component):
    def __init__(self, ascendent):
        super(HeaderLayout, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height / 28) * 4)
        self.setContentsMargins(0, 0, 0, 0)

        self.lbl_location = QLabel()
        self.btn_settings = PopupButton(self, SettingsPopup)

        self.lbl_location.setText(Component.root.settings.settings['site'])
        self.lbl_location.setStyleSheet(Style.replace_variables('font: @SubTextSize @TextFont; \
                                                                font-weight: 30;'))

        map_settings = QPixmap('assets/icons/settings.png')
        self.btn_settings.setIcon(QIcon(map_settings))
        self.btn_settings.setIconSize(QSize(Style.sizes.icon_medium, Style.sizes.icon_medium))

        self.addStretch(1)
        self.addWidget(self.btn_settings)
        self.addStretch(1)
        self.addWidget(self.lbl_location)
        self.addStretch(4)
# SIDE LIST TOGGLE CONTAINER
#   - Button Toggle [WIDGET]
#   - Button List [WIDGET]
class ToggleLayout(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(ToggleLayout, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, (self.height / 28) * 23)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        self.list_toggle = PanelToggle(self, 'Rooms', 'Alerts')

        self.button_list = ButtonList(self)
        self.log_list = LabelList(self)

        self.location_list = QWidget()
        self.location_list.setLayout(self.button_list)

        self.alert_list = QWidget()
        self.alert_list.setLayout(self.log_list)

        list_container = QHBoxLayout()
        list_container.addWidget(self.location_list)
        list_container.addWidget(self.alert_list)

        container_widget = QWidget()
        container_widget.setLayout(list_container)

        self.location_view = False
        self.toggle()

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setAlignment(Qt.AlignTop)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(container_widget)
        self.scroll.setMinimumHeight(self.height - (Style.unit / 4))

        self.addWidget(self.list_toggle)
        self.addWidget(self.scroll)
        self.addStretch(2)

    def show(self):
        self.list_toggle.show()
        if self.location_view:
            self.location_list.show()
            self.alert_list.hide()
        else:
            self.alert_list.show()
            self.location_list.hide()
        self.update()

    def hide(self):
        self.list_toggle.hide()
        self.location_list.hide()
        self.alert_list.hide()

    def toggle(self):
        if self.location_view:
            self.location_view = False
            self.location_list.hide()
            self.alert_list.show()
        else:
            self.location_view = True
            self.alert_list.hide()
            self.location_list.show()
        self.update()

    def add_button(self, label):
        self.button_list.add_button(label)

    def clear(self):
        self.button_list.clear_buttons()
###############################
