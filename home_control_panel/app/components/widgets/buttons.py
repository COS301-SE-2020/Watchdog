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


class ButtonSwitch(QVBoxLayout, Component):
    def __init__(self, ascendent, label):
        super(ButtonSwitch, self).__init__(ascendent=ascendent)
        self.active = False
        self.marker = QHSeperationLine()
        self.button = QPushButton()
        self.button.setText(label)
        self.button.setMinimumHeight(int(Style.unit / 12.8))
        self.marker.setContentsMargins(0, 0, 0, 0)

        self.button.setMinimumWidth(int(Style.unit / 4))

        self.addWidget(self.button)
        self.addWidget(self.marker)

        self.off()

    def draw(self):
        if self.active:
            self.button.setStyleSheet(Style.replace_variables('margin: @None; \
                                        padding: @None; \
                                        margin-top: @PaddingSmall; \
                                        color: @HighlightTextColor;'))
            self.marker.setStyleSheet(Style.replace_variables('background-color: @HighlightColor; \
                                        margin: @None; \
                                        padding: @None;'))
        else:
            self.button.setStyleSheet(Style.replace_variables(('margin: @None; \
                                        padding: @None; \
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


class ButtonToggle(QVBoxLayout, Component):
    def __init__(self, ascendent, left_label, right_label):
        super(ButtonToggle, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        self.toggle_layout = QHBoxLayout()
        self.toggle_layout.setContentsMargins(0, 0, 0, 0)
        self.toggle_layout.setSpacing(0)
        self.toggle_layout.setAlignment(Qt.AlignCenter)

        self.left_button = ButtonSwitch(self, left_label)
        self.left_button.on()

        self.right_button = ButtonSwitch(self, right_label)
        self.right_button.off()

        self.left_button.button.setStyleSheet(Style.replace_variables('border-radius: @PaddingSmall'))
        self.right_button.button.setStyleSheet(Style.replace_variables('border-radius: @PaddingSmall'))

        self.left_container = QWidget()
        self.left_container.setLayout(self.left_button)

        self.right_container = QWidget()
        self.right_container.setLayout(self.right_button)

        self.spacer = QVSeperationLine()

        self.toggle_layout.addWidget(self.left_container)
        self.toggle_layout.addWidget(self.spacer)
        self.toggle_layout.addWidget(self.right_container)

        self.contain_toggle = QWidget()
        self.contain_toggle.setLayout(self.toggle_layout)
        self.contain_toggle.setMinimumHeight(Style.unit / 8)

        self.left_button.setContentsMargins(0, 0, 0, 0)
        self.right_button.setContentsMargins(0, 0, 0, 0)

        self.setAlignment(Qt.AlignCenter)
        self.addWidget(self.contain_toggle)

    def toggle_handler(self):
        self.left_button.toggle()
        self.right_button.toggle()


class CenterToggle(QWidget, Component):
    def __init__(self, ascendent, left_label, right_label):
        super(CenterToggle, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)
<<<<<<< Updated upstream
        self.setStyleSheet(Style.replace_variables('background-color: @AltDarkColor; \
=======
        self.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=8, xOffset=3, yOffset=3))
        self.setStyleSheet(Style.replace_variables('background-color: transparent; \
>>>>>>> Stashed changes
                                                    border-radius: @MediumRadius; \
                                                    margin: @None; \
                                                    padding: @None;'))
        self.toggle = ButtonToggle(ascendent, left_label, right_label)
        self.toggle.left_button.button.clicked.connect(self.toggle_handler)
        self.toggle.right_button.button.clicked.connect(self.toggle_handler)
<<<<<<< Updated upstream
        self.toggle.contain_toggle.setMinimumWidth(Style.unit * 0.6)
        self.toggle.contain_toggle.setMaximumWidth(Style.unit)
        self.toggle.left_container.setStyleSheet(Style.replace_variables('text-align: center; \
                                                    border-radius: @MediumRadius;'))
        self.toggle.right_container.setStyleSheet(Style.replace_variables('text-align: center; \
                                                    border-radius: @MediumRadius;'))
        self.toggle.contain_toggle.setStyleSheet(Style.replace_variables('background-color: @AltDarkColor; \
                                                    margin: @None; \
                                                    padding: @None;'))
        self.toggle.spacer.setStyleSheet(Style.replace_variables('background-color: @LightTextColor; \
                                                    margin: @None;'))
=======

        self.toggle.contain_toggle.setFixedWidth(Style.unit * 0.7)
        self.toggle.contain_toggle.setStyleSheet(Style.replace_variables('background-color: @AltLightColor; \
                                                                        margin: @None; \
                                                                        padding: @None; \
                                                                        border-radius: @MediumRadius;'))
>>>>>>> Stashed changes
        container_layout = QHBoxLayout()
        container_layout.setAlignment(Qt.AlignCenter)
        container_layout.addStretch()
        container_layout.addLayout(self.toggle)
        container_layout.addStretch()

        self.setLayout(container_layout)
<<<<<<< Updated upstream

        self.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=10, xOffset=3, yOffset=3))
=======
>>>>>>> Stashed changes

    def toggle_handler(self):
        Component.root.toggle_grid()
        self.toggle.toggle_handler()
        self.update()


class PanelToggle(QWidget, Component):
    def __init__(self, ascendent, left_label, right_label):
        super(PanelToggle, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(Style.replace_variables('background-color: @AltDarkColor; \
                                                    margin: @None; \
                                                    padding: @None;'))
        self.toggle = ButtonToggle(ascendent, left_label, right_label)
        self.toggle.left_button.button.clicked.connect(self.toggle_handler)
        self.toggle.right_button.button.clicked.connect(self.toggle_handler)
        self.toggle.contain_toggle.setMinimumWidth(self.width)
        self.toggle.left_container.setMinimumWidth(self.width / 2)
        self.toggle.right_container.setMinimumWidth(self.width / 2)
        self.toggle.left_container.setStyleSheet(Style.replace_variables('text-align: center; \
                                                    margin: @None; \
                                                    padding: @None;'))
        self.toggle.right_container.setStyleSheet(Style.replace_variables('text-align: center; \
                                                    margin: @None; \
                                                    padding: @None;'))
        self.toggle.contain_toggle.setStyleSheet(Style.replace_variables('background-color: @AltDarkColor; \
                                                    margin: @None; \
                                                    padding: @None;'))
        self.toggle.spacer.setStyleSheet(Style.replace_variables('background-color: black; \
                                                    margin: @None; \
                                                    padding: @None;'))

        contain_toggle = QHBoxLayout()
        contain_toggle.addStretch(1)
        contain_toggle.addLayout(self.toggle)
        contain_toggle.addStretch(1)
        contain_toggle.setContentsMargins(0, 0, 0, 0)
        contain_toggle.setSpacing(0)

        widget_contain = QWidget()
        widget_contain.setStyleSheet(Style.replace_variables('background-color: @AltDarkColor; \
                                                        margin: @None; \
                                                        padding: @None;'))
        widget_contain.setLayout(contain_toggle)

        contain_layout = QHBoxLayout()
        contain_layout.addWidget(widget_contain)
        contain_layout.setSpacing(0)
        contain_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(contain_layout)

        self.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=10, xOffset=5, yOffset=5))

    def toggle_handler(self):
        Component.root.toggle_list()
        self.toggle.toggle_handler()
        self.update()


class ListButton(QPushButton, Component):
    def __init__(self, label, ascendent=None):
        super(ListButton, self).__init__(ascendent=ascendent)
        self.label = label
        self.setContentsMargins(0, 0, 0, 0)
        self.clicked.connect(self.toggle_handler)

    def toggle_handler(self):
        Component.root.change_location(self.label)
