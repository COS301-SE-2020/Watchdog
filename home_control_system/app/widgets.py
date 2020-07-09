from PyQt5.QtCore import (
    Qt,
    QSize,
    QPoint
)
from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QWidget,
    QLineEdit,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QSizePolicy,
    QRadioButton,
    QGraphicsDropShadowEffect
)
from PyQt5.QtGui import (
    QIcon,
    QImage,
    QPixmap,
    QPainter
)
# from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
# from PyQt5.QtMultimediaWidgets import QVideoWidget
# from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QStatusBar)
from .component import Component
from .styles import Style

class StreamView(QWidget):
    def __init__(self, parent=None, location='', address=''):
        super(StreamView, self).__init__(parent)
        self.qp = QPainter()
        self.image = QImage()
        self.location = location
        self.address = address
        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumWidth(Style.unit)
        self.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))

    def set_frame(self, frame):
        if frame is not None:
            del self.image
            height, width, bpc = frame.shape
            bpl = bpc * width
            self.image = QImage(frame.data, width, height, bpl, QImage.Format_RGB888)
            self.setFixedSize(self.image.size())
            self.update()

    def paintEvent(self, event):
        self.qp.begin(self)
        if self.image:
            self.qp.drawImage(QPoint(0, 0), self.image)
        self.qp.end()


class StreamGrid(QGridLayout, Component):
    def __init__(self, ascendent):
        super(StreamGrid, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
        self.setAlignment(Qt.AlignLeft)
        (self.row, self.col) = (0, 0)
        self.views = []
        self.append_plus()
    
    def append_plus(self):
        if self.col >= 3:
            self.row += 1
            self.col = 0

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
        btn_holder_out.addWidget(btn_container_in)

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
        inner_layout.addStretch()

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        outer_layout.setAlignment(Qt.AlignCenter)
        outer_layout.addLayout(inner_layout)
        outer_layout.addStretch()

        layout_container = QWidget()
        layout_container.setContentsMargins(0, 0, 0, 0)
        layout_container.setLayout(outer_layout)
        layout_container.setMaximumWidth(Style.unit + int(Style.unit / 4))
        layout_container.setMaximumHeight(Style.unit)
        layout_container.setStyleSheet(Style.replace_variables('border: @None; \
                                                                margin: @None; \
                                                                padding: @None;'))
        self.addWidget(layout_container, self.row, self.col)
        self.setRowMinimumHeight(self.row, (Style.unit * 0.6) + int(Style.unit / 8))

        self.views.append(layout_container)
        self.col += 1

    def remove_view(self, index):
        self.removeWidget(self.views[index])
        self.views[index].deleteLater()
        del self.views[index]
        self.col -= 1
        if self.col < 0:
            self.row -= 1
            self.col = 2

    def add_view(self, camera):
        self.remove_view(len(self.views) - 1)

        if self.col >= 3:
            self.row += 1
            self.col = 0

        view = StreamView(location=camera.location, address=camera.address)

        lbl_address = QLabel()
        lbl_address.setContentsMargins(0, 0, 0, 0)
        lbl_address.setText(view.address)
        lbl_address.setAlignment(Qt.AlignLeft)
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
        lbl_location.setAlignment(Qt.AlignLeft)
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
        layout_address.setAlignment(Qt.AlignCenter)

        icon = QLabel()
        map_logo = QPixmap('assets/icons/signal_off.png')
        icon.setPixmap(map_logo.scaled(10, 10, Qt.KeepAspectRatio, Qt.FastTransformation))
        icon.setStyleSheet(Style.replace_variables('margin: @None; \
                                                    padding: @None; \
                                                    background-color: @LightColor;'))
        layout_address.addWidget(icon)
        layout_address.addWidget(lbl_address)

        layout_location = QHBoxLayout()
        layout_location.setAlignment(Qt.AlignCenter)
        icon = QLabel()
        map_logo = QPixmap('assets/icons/signal_off.png')
        icon.setPixmap(map_logo.scaled(10, 10, Qt.KeepAspectRatio, Qt.FastTransformation))
        icon.setStyleSheet(Style.replace_variables('margin: @None; \
                                                    padding: @None; \
                                                    background-color: @LightColor;'))
        layout_location.addWidget(icon)
        layout_location.addWidget(lbl_location)

        inner_layout.addWidget(view)
        inner_layout.addLayout(layout_address)
        inner_layout.addLayout(layout_location)
        inner_layout.addStretch(1)
        outer_layout.addLayout(inner_layout)
        outer_layout.addStretch(1)

        layout_container = QWidget()
        layout_container.setLayout(outer_layout)
        self.addWidget(layout_container, self.row, self.col)
        self.setRowMinimumHeight(self.row, (Style.unit * 0.6) + int(Style.unit / 8))
        self.views.append(layout_container)
        self.col += 1

        self.append_plus()

        self.update()

        camera.stream.add_stream_view(view, (Style.unit, Style.unit * 0.6))

    def clear_views(self):
        print('Clearing Views')
        for index in range(len(self.views)):
            self.remove_view(index)
        (self.row, self.col) = (0, 0)
        self.views = []
        self.update()

    def add_views(self, cameras):
        print('Adding Views')
        for index in range(len(cameras)):
            self.add_view(cameras[index])
        self.update()


class CenterToggle(QWidget, Component):
    def __init__(self, ascendent, left_label, right_label):
        super(CenterToggle, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(Style.replace_variables('background-color: @LightColor; \
                                                    border-radius: @MediumRadius; \
                                                    margin: @None; \
                                                    padding: @None;'))
        self.toggle = ButtonToggle(ascendent, left_label, right_label)
        self.toggle.contain_toggle.setMinimumWidth(Style.unit * 0.6)
        self.toggle.contain_toggle.setMaximumWidth(Style.unit)
        self.toggle.left_button.setContentsMargins(0, 0, (Style.unit / 14), 0)
        self.toggle.right_button.setContentsMargins((Style.unit / 14), 0, 0, 0)
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


class PanelToggle(QWidget, Component):
    def __init__(self, ascendent, left_label, right_label):
        super(PanelToggle, self).__init__(ascendent=ascendent)
        self.setMinimumWidth(self.width)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(Style.replace_variables('background-color: @LightColor; \
                                                    margin: @None; \
                                                    padding: @None;'))
        self.toggle = ButtonToggle(ascendent, left_label, right_label)
        self.toggle.contain_toggle.setMinimumWidth(self.width)
        self.toggle.left_container.setMinimumWidth(self.width / 2)
        self.toggle.right_container.setMinimumWidth(self.width / 2)
        # self.toggle.left_container.setMinimumHeight(self.height)
        # self.toggle.right_container.setMinimumHeight(self.height)
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
        self.left_button.button.clicked.connect(self.toggle_handler)

        self.right_button = ButtonSwitch(self, right_label)
        self.right_button.off()
        self.right_button.button.clicked.connect(self.toggle_handler)

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


class ButtonSwitch(QVBoxLayout, Component):
    def __init__(self, ascendent, label):
        super(ButtonSwitch, self).__init__(ascendent=ascendent)
        self.active = False
        self.marker = QHSeperationLine()
        self.button = QPushButton()
        self.button.setText(label)
        self.button.setMinimumHeight(int(Style.unit / 12.8))
        self.marker.setContentsMargins(0, 0, 0, 0)

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

        btn = QPushButton()
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
        btn.clicked.connect(lambda: self.toggle_handler(self.buttons.index(btn)))

        self.addWidget(btn)
        self.addWidget(seperator)

        self.toggle_handler(0)

        self.append_plus()

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

        layout_container.setStyleSheet(Style.replace_variables('margin: @None; padding: @None;'))

        self.buttons.append(layout_container)
        self.addWidget(layout_container)

    def toggle_handler(self, btn_index):
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


class QHSeperationLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(Style.replace_variables('background-color: @LightTextColor;'))
        self.setMinimumWidth(1)
        self.setFixedHeight(1)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)


class QVSeperationLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(Style.replace_variables('background-color: @LightTextColor;'))
        self.setFixedWidth(1)
        self.setMinimumHeight(1)
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)


class PopupButton(QPushButton, Component):
    def __init__(self, ascendent, popup_class):
        super(PopupButton, self).__init__(ascendent=ascendent)
        self.clicked.connect(self.buildPopup)
        self.popup = popup_class(ascendent=self)

    def buildPopup(self):
        self.popup.show()

class Popup(QWidget, Component):
    def __init__(self, ascendent):
        super(Popup, self).__init__(ascendent=ascendent)
        self.setWindowFlags(Qt.WindowFlags(Qt.FramelessWindowHint))
        self.setStyleSheet(Style.replace_variables(Style.light))
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        top_margin = Style.unit * 1.5
        left_margin = Style.unit * 2.5
        main_height = int(3 * Style.unit)
        main_width = int(5 * Style.unit)
        popup_width = int(Style.unit * 2)
        self.setGeometry(left_margin + (main_width / 2) - (popup_width / 2), top_margin + (main_height / 2) - (popup_width / 2), popup_width, popup_width)

    def submit(self):
        self.hide()

    def cancel(self):
        self.hide()


class SettingsPopup(Popup):
    def __init__(self, ascendent):
        super(SettingsPopup, self).__init__(ascendent=ascendent)

        vbox = QVBoxLayout()
        vbox.addWidget(QLineEdit())
        vbox.addWidget(QLineEdit())

        hbox = QHBoxLayout()
        hbox.addWidget(QRadioButton('Broadcast'))
        hbox.addWidget(QRadioButton('Network'))
        hbox.addWidget(QRadioButton('Off'))
        hbox.addStretch()

        self.btn_submit = QPushButton('Submit')
        self.btn_cancel = QPushButton('Cancel')

        self.btn_submit.setFixedWidth(int(Style.unit / 3))
        self.btn_cancel.setFixedWidth(int(Style.unit / 3))
        self.btn_submit.clicked.connect(self.submit)
        self.btn_cancel.clicked.connect(self.cancel)

        hbox_click = QHBoxLayout()
        hbox_click.addWidget(self.btn_submit)
        hbox_click.addWidget(self.btn_cancel)
        hbox_click.addStretch()

        self.lbl_location = QLabel('Location')
        self.lbl_address = QLabel('Address')
        self.lbl_streaming = QLabel('Streaming')
        self.lbl_empty = QLabel()

        self.lbl_location.setStyleSheet(Style.replace_variables('border: @None;'))
        self.lbl_address.setStyleSheet(Style.replace_variables('border: @None;'))
        self.lbl_streaming.setStyleSheet(Style.replace_variables('border: @None;'))
        self.lbl_empty.setStyleSheet(Style.replace_variables('border: @None;'))

        self.layout = QFormLayout()
        self.layout.setAlignment(Qt.AlignRight)
        self.layout.addRow(self.lbl_location, QLineEdit('Home'))
        self.layout.addRow(self.lbl_address, vbox)
        self.layout.addRow(self.lbl_streaming, hbox)
        self.layout.addRow(self.lbl_empty, hbox_click)

        layout_center = QVBoxLayout()
        layout_center.setAlignment(Qt.AlignCenter)
        layout_center.addLayout(self.layout)
        
        contain_form = QWidget()
        contain_form.setLayout(layout_center)
        contain_form.setMinimumHeight(int(Style.unit * 2))
        contain_form.setStyleSheet(Style.replace_variables('margin: @MediumMargin; \
                                                            padding: @LargePadding; \
                                                            border: @BorderThick solid @LightTextColor; \
                                                            border-radius: @SmallRadius; \
                                                            background-color: @LightColor; \
                                                            color: @LightTextColor; \
                                                            font: @ButtonTextSize @TextFont; \
                                                            font-weight: 30;'))
        layout_form = QHBoxLayout()
        layout_form.addStretch()
        layout_form.addWidget(contain_form)
        layout_form.addStretch()

        self.setLayout(layout_form)


class CameraPopup(Popup):
    def __init__(self, ascendent):
        super(CameraPopup, self).__init__(ascendent=ascendent)

        vbox = QVBoxLayout()
        vbox.addWidget(QLineEdit())
        vbox.addWidget(QLineEdit())

        hbox = QHBoxLayout()
        hbox.addWidget(QRadioButton('Broadcast'))
        hbox.addWidget(QRadioButton('Network'))
        hbox.addWidget(QRadioButton('Off'))
        hbox.addStretch()

        self.btn_submit = QPushButton('Submit')
        self.btn_cancel = QPushButton('Cancel')

        self.btn_submit.setFixedWidth(int(Style.unit / 3))
        self.btn_cancel.setFixedWidth(int(Style.unit / 3))
        self.btn_submit.clicked.connect(self.submit)
        self.btn_cancel.clicked.connect(self.cancel)

        hbox_click = QHBoxLayout()
        hbox_click.addWidget(self.btn_submit)
        hbox_click.addWidget(self.btn_cancel)
        hbox_click.addStretch()

        self.lbl_id = QLabel('Camera ID')
        self.lbl_location = QLabel('Location')
        self.lbl_address = QLabel('IP Address')
        self.lbl_port = QLabel('Port')
        self.lbl_protocol = QLabel('Protocol')
        self.lbl_path = QLabel('Path (Optional)')
        self.lbl_empty = QLabel()

        self.lbl_id.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_location.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_address.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_port.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_protocol.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_path.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_empty.setStyleSheet(Style.replace_variables('border: @None'))

        self.input_id = QLabel(str(len(Component.root.cameras)))
        self.input_id.setStyleSheet(Style.replace_variables('border: @None'))

        self.input_location = QLineEdit('Sample Video')
        self.input_address = QLineEdit('data/sample/surveillance1.mp4')
        self.input_port = QLineEdit('')
        self.input_protocol = QLineEdit('')
        self.input_path = QLineEdit('')

        self.layout = QFormLayout()
        self.layout.setAlignment(Qt.AlignRight)
        self.layout.addRow(self.lbl_id, self.input_id)
        self.layout.addRow(self.lbl_location, self.input_location)
        self.layout.addRow(self.lbl_address, self.input_address)
        self.layout.addRow(self.lbl_port, self.input_port)
        self.layout.addRow(self.lbl_protocol, self.input_protocol)
        self.layout.addRow(self.lbl_path, self.input_path)
        self.layout.addRow(self.lbl_empty, hbox_click)

        layout_center = QVBoxLayout()
        layout_center.setAlignment(Qt.AlignCenter)
        layout_center.addLayout(self.layout)

        contain_form = QWidget()
        contain_form.setLayout(layout_center)
        contain_form.setMinimumHeight(int(Style.unit * 2))
        contain_form.setStyleSheet(Style.replace_variables('margin: @MediumMargin; \
                                    padding: @LargePadding; \
                                    border: @BorderThick solid @LightTextColor; \
                                    border-radius: @SmallRadius; \
                                    background-color: @LightColor; \
                                    color: @LightTextColor; \
                                    font: @ButtonTextSize @TextFont; \
                                    font-weight: 30;'))

        layout_form = QHBoxLayout()
        layout_form.addStretch()
        layout_form.addWidget(contain_form)
        layout_form.addStretch()

        self.setLayout(layout_form)

    def submit(self):
        self.complete()
        self.hide()

    def cancel(self):
        self.hide()

    def complete(self):
        Component.root.add_camera(
            self.input_id.text(),
            self.input_address.text(),
            self.input_port.text(),
            self.input_path.text(),
            self.input_location.text(),
            self.input_protocol.text()
        )


class LocationPopup(Popup):
    def __init__(self, ascendent):
        super(LocationPopup, self).__init__(ascendent=ascendent)

        self.btn_submit = QPushButton('Submit')
        self.btn_cancel = QPushButton('Cancel')

        self.btn_submit.setFixedWidth(int(Style.unit / 3))
        self.btn_cancel.setFixedWidth(int(Style.unit / 3))
        self.btn_submit.clicked.connect(self.submit)
        self.btn_cancel.clicked.connect(self.cancel)

        hbox = QHBoxLayout()
        hbox.addWidget(QRadioButton('Broadcast'))
        hbox.addWidget(QRadioButton('Network'))
        hbox.addWidget(QRadioButton('Off'))
        hbox.addStretch()

        hbox_click = QHBoxLayout()
        hbox_click.addWidget(self.btn_submit)
        hbox_click.addWidget(self.btn_cancel)
        hbox_click.addStretch()

        self.lbl_id = QLabel('Location ID')
        self.lbl_location = QLabel('Location Name')
        self.lbl_address = QLabel('Priority Level (5)')
        self.lbl_streaming = QLabel('Streaming')
        self.lbl_empty = QLabel()

        self.lbl_id.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_location.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_address.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_streaming.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_empty.setStyleSheet(Style.replace_variables('border: @None'))

        self.input_id = QLabel(str(len(Component.root.locations)))
        self.input_id.setStyleSheet(Style.replace_variables('border: @None'))
        self.input_location = QLineEdit('Room')
        self.input_priority = QLineEdit('5')

        self.layout = QFormLayout()
        self.layout.setAlignment(Qt.AlignRight)
        self.layout.addRow(self.lbl_id, self.input_id)
        self.layout.addRow(self.lbl_location, self.input_location)
        self.layout.addRow(self.lbl_address, self.input_priority)
        self.layout.addRow(self.lbl_streaming, hbox)
        self.layout.addRow(self.lbl_empty, hbox_click)

        layout_center = QVBoxLayout()
        layout_center.setAlignment(Qt.AlignCenter)
        layout_center.addLayout(self.layout)
        
        contain_form = QWidget()
        contain_form.setLayout(layout_center)
        contain_form.setMinimumHeight(int(Style.unit * 2))
        contain_form.setStyleSheet(Style.replace_variables('margin: @MediumMargin; \
                                    padding: @LargePadding; \
                                    border: @BorderThick solid @LightTextColor; \
                                    border-radius: @SmallRadius; \
                                    background-color: @LightColor; \
                                    color: @LightTextColor; \
                                    font: @ButtonTextSize @TextFont; \
                                    font-weight: 30;'))
        layout_form = QHBoxLayout()
        layout_form.addStretch()
        layout_form.addWidget(contain_form)
        layout_form.addStretch()

        self.setLayout(layout_form)

    def submit(self):
        self.complete()
        self.hide()

    def cancel(self):
        self.hide()

    def complete(self):
        Component.root.add_location(
            self.input_id.text(),
            self.input_location.text()
        )


class PlusButton(PopupButton):
    def __init__(self, ascendent, popup_class=Popup):
        super(PlusButton, self).__init__(ascendent=ascendent, popup_class=popup_class)
        map_plus = QPixmap('assets/icons/plus.png')
        self.setIcon(QIcon(map_plus))
        self.setIconSize(QSize(Style.sizes.icon_small, Style.sizes.icon_small))
        self.setStyleSheet('border: @None; margin: @None; padding: @None;')
