from cv2 import resize
from PyQt5.QtCore import (
    Qt,
    QSize,
    QPoint
)
from PyQt5.QtGui import (
    QIcon,
    QImage,
    QPixmap,
    QPainter
)
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QGraphicsDropShadowEffect,
    QAction
)
from .component import Component
from .style import Style
from .popups import (
    Popup,
    PopupButton,
    LocationPopup,
    CameraPopup
)
from .spacers import (
    QHSeperationLine,
    QVSeperationLine
)


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
                                        color: @HighlightColor;'))
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
        self.setStyleSheet(Style.replace_variables('background-color: @LightColor; \
                                                    border-radius: @MediumRadius; \
                                                    margin: @None; \
                                                    padding: @None;'))
        self.toggle = ButtonToggle(ascendent, left_label, right_label)
        self.toggle.left_button.button.clicked.connect(self.toggle_handler)
        self.toggle.right_button.button.clicked.connect(self.toggle_handler)
        self.toggle.contain_toggle.setMinimumWidth(Style.unit * 0.6)
        self.toggle.contain_toggle.setMaximumWidth(Style.unit)
        self.toggle.left_container.setStyleSheet(Style.replace_variables('text-align: center; \
                                                    border-radius: @MediumRadius;'))
        self.toggle.right_container.setStyleSheet(Style.replace_variables('text-align: center; \
                                                    border-radius: @MediumRadius;'))
        self.toggle.contain_toggle.setStyleSheet(Style.replace_variables('background-color: @LightColor; \
                                                    margin: @None; \
                                                    padding: @None;'))
        self.toggle.spacer.setStyleSheet(Style.replace_variables('background-color: @LightTextColor; \
                                                    margin: @None;'))
        container_layout = QHBoxLayout()
        container_layout.setAlignment(Qt.AlignCenter)
        container_layout.addStretch()
        container_layout.addLayout(self.toggle)
        container_layout.addStretch()
        self.setLayout(container_layout)

    def toggle_handler(self):
        Component.root.window.home.view.grid.toggle()
        self.toggle.toggle_handler()
        self.update()


class PanelToggle(QWidget, Component):
    def __init__(self, ascendent, left_label, right_label):
        super(PanelToggle, self).__init__(ascendent=ascendent)
        self.setMinimumWidth(self.width)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(Style.replace_variables('background-color: @LightColor; \
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
        self.toggle.contain_toggle.setStyleSheet(Style.replace_variables('background-color: @LightColor; \
                                                    margin: @None; \
                                                    padding: @None;'))
        self.toggle.spacer.setStyleSheet(Style.replace_variables('background-color: black; \
                                                    margin: @None; \
                                                    padding: @None;'))
        self.setLayout(self.toggle)

    def toggle_handler(self):
        Component.root.window.home.sidepanel.list.toggle()
        self.toggle.toggle_handler()
        self.update()


class ListButton(QPushButton, Component):
    def __init__(self, index, ascendent=None):
        super(ListButton, self).__init__(ascendent=ascendent)
        self.index = index
        self.clicked.connect(self.toggle_handler)

    def toggle_handler(self):
        self.ascendent.toggle_handler(self.index)

class ButtonList(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(ButtonList, self).__init__(ascendent=ascendent)
        self.setAlignment(Qt.AlignTop)
        self.buttons = []
        self.highlights = []
        self.active_index = 0
        self.append_plus()

    def add_button(self, label):
        if len(self.buttons) > 0:
            index = len(self.buttons) - 1
            self.removeWidget(self.buttons[index])
            self.buttons[index].deleteLater()
            del self.buttons[index]

        btn = ListButton(len(self.highlights), self)
        btn.setText(label)
        btn.setFixedHeight(Style.unit / 4 * 0.8)
        btn.setMinimumWidth(self.width * 0.9)

        seperator = QHSeperationLine()

        btn.setStyleSheet(Style.replace_variables('margin-left: @LargeMargin; \
                                font: @ButtonTextSize @TextFont; \
                                font-weight: 15; \
                                color: @LightTextColor;'))
        seperator.setStyleSheet(Style.replace_variables('padding-left: @MediumPadding; \
                                padding-right: @MediumPadding; \
                                background-color: @DarkColor;'))

        self.buttons.append(btn)
        self.highlights.append(seperator)

        self.addWidget(btn)
        
        self.addWidget(seperator)

        self.append_plus()

        self.toggle_handler(0)

    def append_plus(self):
        btn = PlusButton(self, LocationPopup)
        btn.setContentsMargins(0, 0, 0, 0)

        btn_holder = QHBoxLayout()
        btn_holder.setAlignment(Qt.AlignCenter)
        btn_holder.addStretch()
        btn_holder.addWidget(btn)
        btn_holder.addStretch()
        btn_holder.setContentsMargins(0, 0, 0, 0)
        btn_holder.setSpacing(0)

        btn_container = QWidget()
        btn_container.setLayout(btn_holder)

        inner_layout = QHBoxLayout()
        inner_layout.setAlignment(Qt.AlignCenter)
        inner_layout.addWidget(btn_container)

        outer_layout = QVBoxLayout()
        outer_layout.setAlignment(Qt.AlignCenter)
        outer_layout.addLayout(inner_layout)

        layout_container = QWidget()
        layout_container.setLayout(outer_layout)

        layout_container.setStyleSheet(Style.replace_variables('margin: @None; padding-top: @PaddingMedium;'))

        self.buttons.append(layout_container)
        self.addWidget(layout_container)

    def toggle_handler(self, btn_index):
        if len(self.buttons) > 0:
            self.buttons[self.active_index].setStyleSheet(Style.replace_variables('margin-left: @LargeMargin; \
                                                            font: @ButtonTextSize @TextFont; \
                                                            font-weight: 15; \
                                                            color: @LightTextColor;'))
            if self.highlights[self.active_index] is not None:
                self.highlights[self.active_index].setStyleSheet(Style.replace_variables('padding-left: @MediumPadding; \
                                                            padding-right: @MediumPadding; \
                                                            background-color: @DarkColor;'))

            self.buttons[btn_index].setStyleSheet(Style.replace_variables('margin-left: @LargeMargin; \
                                                            font: @ButtonTextSize @TextFont; \
                                                            font-weight: 15; \
                                                            color: @HighlightColor;'))
            if self.highlights[btn_index] is not None:
                self.highlights[btn_index].setStyleSheet(Style.replace_variables('padding-left: @MediumPadding; \
                                                            padding-right: @MediumPadding; \
                                                            background-color: @HighlightColor;'))
            self.active_index = btn_index
            Component.root.list.changeActive(self.active_index)


class StreamView(QWidget):
    count = 0

    def __init__(self, camera, parent=None):
        super(StreamView, self).__init__(parent)
        self.id = StreamView.count
        self.qp = QPainter()
        self.image = QImage()
        self.camera = camera
        self.location = camera.location
        self.address = camera.address
        self.dimensions = (int(Style.unit), int(Style.unit * 0.6))
        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumWidth(Style.unit)
        self.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))
        StreamView.count += 1

        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        quitAction = QAction("Remove", self)
        # quitAction.triggered.connect(qApp.quit)
        self.addAction(quitAction)

    def set_frame(self):
        if self.camera.stream.current_frame is not None:
            frame = resize(self.camera.stream.current_frame, self.dimensions)
            height, width, bpc = frame.shape
            bpl = bpc * width
            self.image = QImage(frame.data, width, height, bpl, QImage.Format_RGB888)
            self.setFixedSize(self.image.size())
            self.update()

    def paintEvent(self, event):
        try:
            self.qp.begin(self)
            if self.image:
                self.qp.drawImage(QPoint(0, 0), self.image)
            self.qp.end()
        except Exception:
            return


class StreamGrid(QGridLayout, Component):
    def __init__(self, ascendent):
        super(StreamGrid, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
        self.setAlignment(Qt.AlignLeft)
        (self.row, self.col) = (0, 0)
        self.views = []
        self.streams = []

    def refresh(self):
        for index in range(len(self.streams)):
            self.streams[index].set_frame()

    def append_plus(self):
        if self.col >= 3:
            self.row += 1
            self.col = 0
        elif self.col < 0:
            self.row -= max(1, 0)
            self.col = max(2, 0)

        btn = PlusButton(self, CameraPopup)
        btn.setStyleSheet('border: @None; margin: @None; padding: @None;')
        btn.setContentsMargins(0, 0, 0, 0)
        btn_holder = QVBoxLayout()
        btn_holder.setAlignment(Qt.AlignCenter)
        btn_holder.addWidget(btn)

        btn_container_in = QWidget()
        btn_container_in.setContentsMargins(0, 0, 0, 0)
        btn_container_in.setLayout(btn_holder)
        btn_container_in.setFixedWidth(Style.unit * 0.7)
        btn_container_in.setFixedHeight(Style.unit * 0.5)
        btn_container_in.setStyleSheet(Style.replace_variables('border: @None; \
                                                            margin: @None; \
                                                            padding: @None;'))
        btn_holder_out = QHBoxLayout()
        btn_holder_out.setContentsMargins(0, 0, 0, 0)
        btn_holder_out.setSpacing(0)
        btn_holder_out.setAlignment(Qt.AlignCenter)
        btn_holder_out.addStretch()
        btn_holder_out.addWidget(btn_container_in)
        btn_holder_out.addStretch()

        btn_container = QWidget()
        btn_container.setContentsMargins(0, 0, 0, 0)
        btn_container.setLayout(btn_holder_out)
        btn_container.setFixedWidth(Style.unit * 0.8)
        btn_container.setFixedHeight(Style.unit * 0.6)
        btn_container.setStyleSheet(Style.replace_variables('border: @BorderThin solid @LightTextColor; \
                                                            margin: @None; \
                                                            padding: @None;'))
        btn_container.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))

        inner_layout = QHBoxLayout()
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.setSpacing(0)
        inner_layout.setAlignment(Qt.AlignCenter)
        inner_layout.addWidget(btn_container)

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        outer_layout.setAlignment(Qt.AlignTop)
        outer_layout.addLayout(inner_layout)

        centre_layout = QVBoxLayout()
        centre_layout.setContentsMargins(0, 0, 0, 0)
        centre_layout.setSpacing(0)
        centre_layout.setAlignment(Qt.AlignLeft)
        centre_layout.addLayout(outer_layout)

        layout_container = QWidget()
        layout_container.setContentsMargins(0, 0, 0, 0)
        layout_container.setLayout(centre_layout)
        layout_container.setMaximumWidth(Style.unit + int(Style.unit / 4))
        layout_container.setStyleSheet(Style.replace_variables('border: @None; \
                                                                margin: @None; \
                                                                padding: @None;'))
        self.addWidget(layout_container, self.row, self.col)
        self.setRowMinimumHeight(self.row, (Style.unit * 0.6) + int(Style.unit / 8))

        self.views.append(layout_container)
        self.col += 1

        self.update()

    def add_view(self, camera, append=True):
        if append and len(self.views) > 0:
            self.remove_view(len(self.views) - 1)

        if self.col >= 3:
            self.row += 1
            self.col = 0
        elif self.col < 0:
            self.row -= max(1, 0)
            self.col = max(2, 0)

        view = StreamView(camera)
        self.streams.append(view)

        lbl_address = QLabel()
        lbl_address.setContentsMargins(0, 0, 0, 0)
        lbl_address.setText(view.address)
        lbl_address.setAlignment(Qt.AlignCenter)
        lbl_address.setStyleSheet(Style.replace_variables('font: @SmallTextSize @TextFont; \
                                                            font-weight: 10; \
                                                            background: none; \
                                                            color: @LightTextColor; \
                                                            margin: @None; \
                                                            padding: @None; \
                                                            margin-top: @MarginSmall;'))
        lbl_location = QLabel()
        lbl_location.setContentsMargins(0, 0, 0, 0)
        lbl_location.setText(view.location)
        lbl_location.setAlignment(Qt.AlignCenter)
        lbl_location.setStyleSheet(Style.replace_variables('font: @SmallTextSize @TextFont; \
                                                            font-weight: 10; \
                                                            background: none; \
                                                            color: @LightTextColor; \
                                                            margin: @None; \
                                                            padding: @None; \
                                                            margin-top: @MarginSmall;'))
        outer_layout = QHBoxLayout()
        outer_layout.setAlignment(Qt.AlignCenter)
        inner_layout = QVBoxLayout()
        inner_layout.setAlignment(Qt.AlignCenter)

        layout_address = QHBoxLayout()
        layout_address.setAlignment(Qt.AlignLeft)
        layout_location = QHBoxLayout()
        layout_location.setAlignment(Qt.AlignLeft)

        icon = QLabel()
        map_logo = QPixmap('assets/icons/signal_off.png')
        icon.setPixmap(map_logo.scaled(10, 10, Qt.KeepAspectRatio, Qt.FastTransformation))
        icon.setStyleSheet(Style.replace_variables('margin: @None; \
                                                    padding: @None; \
                                                    background-color: @LightColor;'))
        layout_address.addWidget(icon)
        layout_address.addWidget(lbl_address)

        icon = QLabel()
        map_logo = QPixmap('assets/icons/signal_off.png')
        icon.setPixmap(map_logo.scaled(10, 10, Qt.KeepAspectRatio, Qt.FastTransformation))
        icon.setStyleSheet(Style.replace_variables('margin: @None; \
                                                    padding: @None; \
                                                    background-color: @LightColor;'))
        layout_location.addWidget(icon)
        layout_location.addWidget(lbl_location)

        info_layout = QVBoxLayout()
        info_layout.addLayout(layout_address)
        info_layout.addLayout(layout_location)

        info_widget = QWidget()
        info_widget.setLayout(info_layout)
        info_widget.setContentsMargins(int(Style.unit / 8), Style.sizes.margin_small, 0, 0)

        inner_layout.addWidget(view)
        inner_layout.addWidget(info_widget)
        outer_layout.addLayout(inner_layout)

        layout_container = QWidget()
        layout_container.setMaximumWidth(Style.unit + int(Style.unit / 4))
        layout_container.setLayout(outer_layout)
        self.addWidget(layout_container, self.row, self.col)
        self.setRowMinimumHeight(self.row, (Style.unit * 0.6) + int(Style.unit / 8))
        self.views.append(layout_container)

        if append:
            self.append_plus()

        self.col += 1

        self.update()

    def remove_view(self, index):
        if self.col >= 3:
            self.row += 1
            self.col = 0
        elif self.col < 0:
            self.row -= 1
            self.col = 2
        if 0 <= index and index < len(self.streams) and self.streams[index] is not None:
            del self.streams[index]
        if 0 <= index and index < len(self.views) and self.views[index] is not None:
            self.removeWidget(self.views[index])
            self.views[index].deleteLater()
            del self.views[index]
            self.col -= 1

    def clear_views(self):
        while len(self.views) > 0:
            self.remove_view(0)
        (self.row, self.col) = (0, 0)
        self.views = []

    def add_views(self, cameras):
        for index in range(len(cameras)):
            self.add_view(cameras[index], False)
        self.append_plus()

    def reset(self, cameras):
        self.clear_views()
        self.add_views(cameras)
        self.update()