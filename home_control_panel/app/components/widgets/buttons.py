from PyQt5.QtCore import (
    Qt,
    QSize
)
from PyQt5.QtGui import (
    QIcon,
    QPixmap
)
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QGraphicsDropShadowEffect
)
from ..component import Component
from ..popups import Popup
from ..style import Style
from .spacers import (
    QHSeperationLine,
    QVSeperationLine
)


class PopupButton(QPushButton, Component):
    def __init__(self, ascendent, popup_class):
        super(PopupButton, self).__init__(ascendent=ascendent)
        self.clicked.connect(self.buildPopup)
        self.popup = popup_class(ascendent=self)

    def buildPopup(self):
        self.popup.show()


class PlusButton(PopupButton):
    def __init__(self, ascendent, popup_class=Popup):
        super(PlusButton, self).__init__(ascendent=ascendent, popup_class=popup_class)
        map_plus = QPixmap('assets/icons/plus.png')
        self.setIcon(QIcon(map_plus))
        self.setIconSize(QSize(Style.sizes.icon_small, Style.sizes.icon_small))
        self.setStyleSheet('border: @None; margin: @None; padding: @None;')


class ButtonSwitch(QWidget, Component):
    def __init__(self, ascendent, label):
        super(ButtonSwitch, self).__init__(ascendent=ascendent)
        self.active = False

        self.marker = QHSeperationLine()
        self.marker.setContentsMargins(0, 0, 0, 0)
        self.button = QPushButton()
        self.button.setContentsMargins(0, 0, 0, 0)

        self.button.setText(label)

        horizontal_box = QHBoxLayout()
        horizontal_box.setSpacing(0)
        horizontal_box.setContentsMargins(0, 0, 0, 0)
        horizontal_box.setAlignment(Qt.AlignCenter)
        horizontal_box.addStretch()
        horizontal_box.addWidget(self.button)
        horizontal_box.addStretch()

        horizontal_widget = QWidget()
        horizontal_widget.setContentsMargins(0, 0, 0, 0)
        horizontal_widget.setLayout(horizontal_box)

        vertical_box = QVBoxLayout()
        vertical_box.setSpacing(0)
        vertical_box.setContentsMargins(0, 0, 0, 0)
        vertical_box.setAlignment(Qt.AlignCenter)
        vertical_box.addStretch()
        vertical_box.addWidget(horizontal_widget)
        vertical_box.addStretch()
        vertical_box.addWidget(self.marker)

        self.setLayout(vertical_box)
        self.setMaximumHeight(int(Style.unit / 10))
        self.setMaximumWidth(int(Style.unit * 0.3))
        self.setContentsMargins(0, 0, 0, 0)

        self.off()

    def draw(self):
        if self.active:
            self.button.setStyleSheet(Style.replace_variables('margin: @None; \
                                        text-align: center; \
                                        padding: @None; \
                                        border-radius: @MediumRadius; \
                                        margin-top: @PaddingSmall; \
                                        color: @HighlightTextColor;'))
            self.marker.setStyleSheet(Style.replace_variables('background-color: @HighlightColor; \
                                        margin: @None; \
                                        padding: @None;'))
        else:
            self.button.setStyleSheet(Style.replace_variables(('margin: @None; \
                                        text-align: center; \
                                        padding: @None; \
                                        border-radius: @MediumRadius; \
                                        margin-top: @PaddingSmall; \
                                        color: @LightTextColor;')))
            self.marker.setStyleSheet(Style.replace_variables(('background-color: @ColorDark; \
                                        margin: @None; \
                                        padding: @None; \
                                        margin-top: @PaddingSmall;')))
        self.update()

    def on(self):
        self.active = True
        self.draw()

    def off(self):
        self.active = False
        self.draw()

    def toggle(self):
        if self.active:
            self.active = False
        else:
            self.active = True
        self.draw()


class ButtonToggle(QWidget, Component):
    def __init__(self, ascendent, left_label, right_label):
        super(ButtonToggle, self).__init__(ascendent=ascendent)
        self.setStyleSheet(Style.replace_variables('margin: @None; padding @SmallPadding;'))
        self.setContentsMargins(0, 0, 0, 0)

        self.toggle_layout = QHBoxLayout()
        self.toggle_layout.setAlignment(Qt.AlignCenter)
        self.toggle_layout.setContentsMargins(0, 0, 0, 0)

        self.left_button = ButtonSwitch(self, left_label)
        self.left_button.on()

        self.right_button = ButtonSwitch(self, right_label)
        self.right_button.off()

        self.spacer = QVSeperationLine()
        self.spacer.setContentsMargins(0, 0, 0, 0)
        self.spacer.setStyleSheet(Style.replace_variables('background-color: @LightColor;'))

        self.toggle_layout.addWidget(self.left_button)
        self.toggle_layout.addWidget(self.spacer)
        self.toggle_layout.addWidget(self.right_button)

        self.contain_toggle = QWidget()
        self.contain_toggle.setLayout(self.toggle_layout)
        self.contain_toggle.setMinimumHeight(Style.unit / 8)
        self.contain_toggle.setContentsMargins(0, 0, 0, 0)
        self.contain_toggle.setStyleSheet(Style.replace_variables('background-color: @AltDarkColor; \
                                                                    border-radius: @MediumRadius; \
                                                                    padding: @None;'))

        vertical_box = QVBoxLayout()
        vertical_box.setAlignment(Qt.AlignCenter)
        vertical_box.addWidget(self.contain_toggle)

        self.setLayout(vertical_box)
        self.setMaximumHeight(int(Style.unit / 6))

    def toggle_handler(self):
        self.left_button.toggle()
        self.right_button.toggle()


class CenterToggle(QWidget, Component):
    def __init__(self, ascendent, left_label, right_label):
        super(CenterToggle, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=10, xOffset=3, yOffset=3))
        self.setStyleSheet(Style.replace_variables('background-color: transparent; \
                                                    border-radius: @MediumRadius; \
                                                    margin: @None; \
                                                    padding: @None;'))

        self.toggle = ButtonToggle(ascendent, left_label, right_label)
        self.toggle.left_button.button.clicked.connect(self.toggle_handler)
        self.toggle.right_button.button.clicked.connect(self.toggle_handler)

        self.toggle.contain_toggle.setFixedWidth(Style.unit * 0.7)
        self.toggle.contain_toggle.setStyleSheet(Style.replace_variables('background-color: @AltLightColor; \
                                                    margin: @None; \
                                                    border-radius: @MediumRadius; \
                                                    padding: @None;'))
        container_layout = QHBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setAlignment(Qt.AlignCenter)
        container_layout.addStretch()
        container_layout.addWidget(self.toggle)
        container_layout.addStretch()

        self.setLayout(container_layout)
        self.setFixedHeight(Style.unit / 6.5)

    def toggle_handler(self):
        Component.root.toggle_grid()
        self.toggle.toggle_handler()
        self.update()


class PanelToggle(QWidget, Component):
    def __init__(self, ascendent, left_label, right_label):
        super(PanelToggle, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=10, xOffset=3, yOffset=3))
        self.setStyleSheet(Style.replace_variables('background-color: transparent; \
                                                    border-radius: @SmallRadius; \
                                                    margin: @None; \
                                                    padding: @None;'))

        self.toggle = ButtonToggle(ascendent, left_label, right_label)
        self.toggle.left_button.button.clicked.connect(self.toggle_handler)
        self.toggle.right_button.button.clicked.connect(self.toggle_handler)

        width = Style.unit * 0.75
        self.toggle.contain_toggle.setMinimumWidth(width)
        self.toggle.left_button.setFixedWidth(width * 0.4)
        self.toggle.right_button.setFixedWidth(width * 0.4)

        container_layout = QHBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setAlignment(Qt.AlignCenter)
        container_layout.addStretch()
        container_layout.addWidget(self.toggle)
        container_layout.addStretch()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(container_layout)

        self.setLayout(layout)
        self.setFixedHeight(Style.unit / 4.5)

    def toggle_handler(self):
        Component.root.toggle_list()
        self.toggle.toggle_handler()
        self.update()


class ListButton(QPushButton, Component):
    def __init__(self, label, ascendent=None):
        super(ListButton, self).__init__(ascendent=ascendent)
        self.label = label
        self.clicked.connect(self.toggle_handler)

    def toggle_handler(self):
        Component.root.change_location(self.label)


class PlayButton(QWidget):
    def __init__(self, view, parent=None):
        super(PlayButton, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)

        self.view = view

        self.button = QPushButton()
        self.button.clicked.connect(self.view.play)

        map_play = QPixmap('assets/icons/play.png')
        self.button.setIcon(QIcon(map_play))
        self.button.setIconSize(QSize(Style.unit / 8, Style.unit / 8))

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()
        layout.addWidget(self.button)
        layout.addStretch()

        self.setLayout(layout)
        self.setMaximumHeight(Style.unit / 8)


class PlayToggleButton(QWidget):
    def __init__(self, view, parent=None):
        super(PlayToggleButton, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)

        self.view = view

        self.button = QPushButton()
        self.button.clicked.connect(self.toggle)

        map_play = QPixmap('assets/icons/play.png')
        self.play_icon = QIcon(map_play)

        map_pause = QPixmap('assets/icons/pause.png')
        self.pause_icon = QIcon(map_pause)

        self.button.setIconSize(QSize(Style.unit / 8, Style.unit / 8))
        self.button.setIcon(self.pause_icon)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()
        layout.addWidget(self.button)
        layout.addStretch()

        self.setLayout(layout)
        self.setMaximumHeight(Style.unit / 8)

    def toggle(self):
        self.view.playing = not self.view.playing
        if self.view.playing:
            self.button.setIcon(self.pause_icon)
        else:
            self.button.setIcon(self.play_icon)
