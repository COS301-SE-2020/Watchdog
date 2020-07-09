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
    def __init__(self, parent=None, location='Outside', address='10.0.0.115'):
        super(StreamView, self).__init__(parent)
        self.image = None
        self.location = location
        self.address = address
        self.setContentsMargins(0, 0, 0, 0)
        self.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))

    def set_frame(self, frame):
        if frame is not None:
            height, width, bpc = frame.shape
            bpl = bpc * width
            self.image = QImage(frame.data, width, height, bpl, QImage.Format_RGB888)
            self.setMinimumSize(self.image.size())
            self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QPoint(0, 0), self.image)
        qp.end()


class StreamGrid(QGridLayout, Component):
    def __init__(self, ascendent):
        super(StreamGrid, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
        self.setAlignment(Qt.AlignLeft)
        (self.row, self.col) = (0, 0)
    
    def append_plus(self):
        btn = PlusButton(self, CameraPopup)
        btn.setContentsMargins(0, 0, 0, 0)

        btn_holder = QVBoxLayout()
        btn_holder.setContentsMargins(0, 0, 0, 0)
        btn_holder.setAlignment(Qt.AlignCenter)
        btn_holder.addStretch()
        btn_holder.addWidget(btn)
        btn_holder.addStretch()

        btn_container = QWidget()
        btn_container.setContentsMargins(0, 0, 0, 0)
        btn_container.setLayout(btn_holder)
        btn_container.setFixedWidth(Style.unit)
        btn_container.setFixedHeight(Style.unit * 0.6)
        btn_container.setStyleSheet(Style.replace_variables('border: 1px solid @LightTextColor; margin: 0px; padding: 0px;'))
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
        outer_layout.setAlignment(Qt.AlignTop)
        outer_layout.addLayout(inner_layout)
        outer_layout.addStretch()

        layout_container = QWidget()
        layout_container.setContentsMargins(0, 0, 0, 0)
        layout_container.setLayout(outer_layout)
        layout_container.setMaximumWidth(Style.unit + int(Style.unit / 8))
        layout_container.setMaximumHeight((Style.unit * 0.6) + int(Style.unit / 8))
        layout_container.setStyleSheet(Style.replace_variables('margin: 0px; padding: 0px;'))

        self.add_view(layout_container)

    def add_view(self, view):
        if self.col >= 3:
            self.row += 1
            self.col = 0
        self.addWidget(view, self.row, self.col)
        self.setRowMinimumHeight(self.row, (Style.unit * 0.6) + int(Style.unit / 8))
        self.col += 1

    def set_views(self, views):
        (self.row, self.col) = (0, 0)
        for index in range(len(views)):
            lbl_address = QLabel()
            lbl_address.setContentsMargins(0, 0, 0, 0)
            lbl_address.setText(views[index].address)
            lbl_address.setAlignment(Qt.AlignLeft)
            lbl_address.setStyleSheet(Style.replace_variables('font: @SmallTextSize Corbel, sans-serif; \
                                                                font-weight: 10; \
                                                                background: none; \
                                                                color: @LightTextColor; \
                                                                margin: 0px; \
                                                                padding: 0px; \
                                                                margin-top: 5px;'))

            lbl_location = QLabel()
            lbl_location.setContentsMargins(0, 0, 0, 0)
            lbl_location.setText(views[index].location)
            lbl_location.setAlignment(Qt.AlignLeft)
            lbl_location.setStyleSheet(Style.replace_variables('font: @SmallTextSize Corbel, sans-serif; \
                                                                font-weight: 10; \
                                                                background: none; \
                                                                color: @LightTextColor; \
                                                                margin: 0px; \
                                                                padding: 0px; \
                                                                margin-top: 5px;'))

            outer_layout = QHBoxLayout()
            outer_layout.setAlignment(Qt.AlignLeft)

            inner_layout = QVBoxLayout()
            inner_layout.setAlignment(Qt.AlignCenter)

            layout_address = QHBoxLayout()
            layout_address.setAlignment(Qt.AlignCenter)

            icon = QLabel()
            map_logo = QPixmap('assets/icons/signal_off.png')
            icon.setPixmap(map_logo.scaled(10, 10, Qt.KeepAspectRatio, Qt.FastTransformation))
            icon.setStyleSheet(Style.replace_variables('margin: 0px; \
                                                        padding: 0px; \
                                                        background-color: @LightColor;'))

            layout_address.addWidget(icon)
            layout_address.addWidget(lbl_address)

            layout_location = QHBoxLayout()
            layout_location.setAlignment(Qt.AlignCenter)

            icon = QLabel()
            map_logo = QPixmap('assets/icons/signal_off.png')
            icon.setPixmap(map_logo.scaled(10, 10, Qt.KeepAspectRatio, Qt.FastTransformation))
            icon.setStyleSheet(Style.replace_variables('margin: 0px; \
                                                        padding: 0px; \
                                                        background-color: @LightColor;'))

            layout_location.addWidget(icon)
            layout_location.addWidget(lbl_location)

            inner_layout.addWidget(views[index])
            inner_layout.addLayout(layout_address)
            inner_layout.addLayout(layout_location)
            inner_layout.addStretch(1)

            outer_layout.addLayout(inner_layout)
            outer_layout.addStretch(1)

            layout_container = QWidget()
            layout_container.setLayout(outer_layout)
            
            self.add_view(layout_container)

        self.append_plus()


class CenterToggle(QWidget, Component):
    def __init__(self, ascendent, left_label, right_label):
        super(CenterToggle, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet(Style.replace_variables('background-color: @LightColor; \
                                                    border-radius: @MediumRadius; \
                                                    margin: 0px; \
                                                    padding: 0px;'))

        self.toggle = ButtonToggle(ascendent, left_label, right_label)

        self.toggle.contain_toggle.setMinimumWidth(Style.unit * 0.6)

        self.toggle.left_container.setStyleSheet(Style.replace_variables('text-align: center; \
                                                    border-radius: @MediumRadius; \
                                                    margin-right: 35px;'))
        self.toggle.right_container.setStyleSheet(Style.replace_variables('text-align: center; \
                                                    border-radius: @MediumRadius; \
                                                    margin-left: 35px;'))
        self.toggle.contain_toggle.setStyleSheet(Style.replace_variables('background-color: @LightColor; \
                                                    margin: 0px; \
                                                    padding: 0px;'))
        self.toggle.spacer.setStyleSheet(Style.replace_variables('background-color: @LightTextColor; \
                                                    margin: 0px; \
                                                    margin-left: 12px;\
                                                    margin-right: 12px;'))

        self.setLayout(self.toggle)


class PanelToggle(QWidget, Component):
    def __init__(self, ascendent, left_label, right_label):
        super(PanelToggle, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)
        self.toggle = ButtonToggle(ascendent, left_label, right_label)

        self.toggle.left_container.setStyleSheet(Style.replace_variables('text-align: center; \
                                                                        margin: 0px; \
                                                                        padding: 0px;'))
        self.toggle.right_container.setStyleSheet(Style.replace_variables('text-align: center; \
                                                                        margin: 0px; \
                                                                        padding: 0px;'))
        self.toggle.contain_toggle.setStyleSheet(Style.replace_variables('background-color: @LightColor; \
                                                                        margin: 0px; \
                                                                        padding: 0px;'))
        self.toggle.spacer.setStyleSheet(Style.replace_variables('background-color: black; \
                                                                        margin: 0px; \
                                                                        padding: 0px;'))

        self.toggle.contain_toggle.setMinimumWidth(self.width)
        self.toggle.left_container.setMinimumWidth(self.width / 2)
        self.toggle.right_container.setMinimumWidth(self.width / 2)

        self.setMinimumWidth(self.width)
        self.setLayout(self.toggle)
        self.setStyleSheet(Style.replace_variables('background-color: @LightColor; \
                            margin: 0px; padding: 0px;'))


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
        self.left_button.setContentsMargins(0, 0, (Style.unit / 14), 0)

        self.right_button = ButtonSwitch(self, right_label)
        self.right_button.off()
        self.right_button.button.clicked.connect(self.toggle_handler)
        self.right_button.setContentsMargins((Style.unit / 14), 0, 0, 0)

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
        self.button.setMinimumHeight(28)
        self.marker.setContentsMargins(0, 0, 0, 0)

        self.addWidget(self.button)
        self.addWidget(self.marker)
        self.off()

    def draw(self):
        if self.active:
            self.button.setStyleSheet(Style.replace_variables('margin: 0px; \
                                        padding: 0px; \
                                        padding-top: 2px; \
                                        color: @HighlightColor;'))
            self.marker.setStyleSheet(Style.replace_variables('background-color: @HighlightColor; \
                                        margin: 0px; \
                                        padding: 0px;'))
        else:
            self.button.setStyleSheet(Style.replace_variables(('margin: 0px; \
                                        padding: 0px; \
                                        padding-top: 2px; \
                                        color: @LightTextColor;')))
            self.marker.setStyleSheet(Style.replace_variables(('background-color: @ColorDark; \
                                        margin: 0px; \
                                        padding: 0px;')))
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

    def addButton(self, label):
        btn = QPushButton()
        btn.setText(label)
        btn.setFixedHeight(Style.unit / 4 * 0.8)
        btn.setMinimumWidth(self.width * 0.9)

        seperator = QHSeperationLine()

        btn.setStyleSheet(Style.replace_variables('margin-left: 35px; \
                                font: ' + Style.text.button + ' Corbel, sans-serif; \
                                font-weight: 15; \
                                color: @LightTextColor;'))
        seperator.setStyleSheet(Style.replace_variables('padding-left: 10px; \
                                padding-right: 10px; \
                                background-color: ' + Style.colors.dark + ';'))

        self.buttons.append(btn)
        self.highlights.append(seperator)
        btn.clicked.connect(lambda: self.toggle_handler(self.buttons.index(btn)))

        self.addWidget(btn)
        self.addWidget(seperator)

        self.toggle_handler(0)

    def addPlus(self):
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

        layout_container.setStyleSheet(Style.replace_variables('margin: 0px; padding: 0px;'))

        self.buttons.append(layout_container)
        self.highlights.append(None)
        self.addWidget(layout_container)

    def toggle_handler(self, btn_index):
        self.buttons[self.active_index].setStyleSheet(Style.replace_variables('margin-left: 35px; \
                                                        font: ' + Style.text.button + ' Corbel, sans-serif; \
                                                        font-weight: 15; \
                                                        color: @LightTextColor;'))
        if self.highlights[self.active_index] is not None:
            self.highlights[self.active_index].setStyleSheet(Style.replace_variables('padding-left: 10px; \
                                                        padding-right: 10px; \
                                                        background-color: ' + Style.colors.dark + ';'))

        self.buttons[btn_index].setStyleSheet(Style.replace_variables('margin-left: 35px; \
                                                        font: ' + Style.text.button + ' Corbel, sans-serif; \
                                                        font-weight: 15; \
                                                        color: ' + Style.colors.highlight + ';'))
        if self.highlights[btn_index] is not None:
            self.highlights[btn_index].setStyleSheet(Style.replace_variables('padding-left: 10px; \
                                                        padding-right: 10px; \
                                                        background-color: ' + Style.colors.highlight + ';'))

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

        self.lbl_location.setStyleSheet(Style.replace_variables('border: 0px solid @LightTextColor;'))
        self.lbl_address.setStyleSheet(Style.replace_variables('border: 0px solid @LightTextColor;'))
        self.lbl_streaming.setStyleSheet(Style.replace_variables('border: 0px solid @LightTextColor;'))
        self.lbl_empty.setStyleSheet(Style.replace_variables('border: 0px solid @LightTextColor;'))

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
        contain_form.setStyleSheet(Style.replace_variables('margin: 15px; \
                                    padding: 15px; \
                                    border: 2px solid @LightTextColor; \
                                    border-radius: @SmallRadius; \
                                    background-color: @LightColor; \
                                    color: @LightTextColor; \
                                    font: ' + Style.text.button + ' Corbel, sans-serif; \
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

        self.lbl_id.setStyleSheet(Style.replace_variables('border: 0px solid @LightTextColor;'))
        self.lbl_empty.setStyleSheet(Style.replace_variables('border: 0px solid @LightTextColor;'))

        self.layout = QFormLayout()
        self.layout.setAlignment(Qt.AlignRight)
        self.layout.addRow(self.lbl_id, QLineEdit('0'))
        self.layout.addRow(self.lbl_location, QLineEdit())
        self.layout.addRow(self.lbl_address, QLineEdit('10.0.0.115'))
        self.layout.addRow(self.lbl_port, QLineEdit('8080'))
        self.layout.addRow(self.lbl_protocol, QLineEdit('rtsp'))
        self.layout.addRow(self.lbl_path, QLineEdit('h264_ulaw.sdp'))
        self.layout.addRow(self.lbl_empty, hbox_click)

        layout_center = QVBoxLayout()
        layout_center.setAlignment(Qt.AlignCenter)
        layout_center.addLayout(self.layout)
        
        contain_form = QWidget()
        contain_form.setLayout(layout_center)
        contain_form.setMinimumHeight(int(Style.unit * 2))
        contain_form.setStyleSheet(Style.replace_variables('margin: 15px; \
                                    padding: 15px; \
                                    border: 2px solid @LightTextColor; \
                                    border-radius: @SmallRadius; \
                                    background-color: @LightColor; \
                                    color: @LightTextColor; \
                                    font: ' + Style.text.button + ' Corbel, sans-serif; \
                                    font-weight: 30;'))

        layout_form = QHBoxLayout()
        layout_form.addStretch()
        layout_form.addWidget(contain_form)
        layout_form.addStretch()

        self.setLayout(layout_form)


class LocationPopup(Popup):
    def __init__(self, ascendent):
        super(LocationPopup, self).__init__(ascendent=ascendent)

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

        self.lbl_location = QLabel('Location Name')
        self.lbl_address = QLabel('Physical Address')
        self.lbl_empty = QLabel()

        self.lbl_location.setStyleSheet(Style.replace_variables('border: 0px solid @LightTextColor;'))
        self.lbl_address.setStyleSheet(Style.replace_variables('border: 0px solid @LightTextColor;'))
        self.lbl_empty.setStyleSheet(Style.replace_variables('border: 0px solid @LightTextColor;'))

        self.layout = QFormLayout()
        self.layout.setAlignment(Qt.AlignRight)
        self.layout.addRow(self.lbl_location, QLineEdit('Home'))
        self.layout.addRow(self.lbl_address, vbox)
        self.layout.addRow(self.lbl_empty, hbox_click)

        layout_center = QVBoxLayout()
        layout_center.setAlignment(Qt.AlignCenter)
        layout_center.addLayout(self.layout)
        
        contain_form = QWidget()
        contain_form.setLayout(layout_center)
        contain_form.setMinimumHeight(int(Style.unit * 2))
        contain_form.setStyleSheet(Style.replace_variables('margin: 15px; \
                                    padding: 15px; \
                                    border: 2px solid @LightTextColor; \
                                    border-radius: @SmallRadius; \
                                    background-color: @LightColor; \
                                    color: @LightTextColor; \
                                    font: ' + Style.text.button + ' Corbel, sans-serif; \
                                    font-weight: 30;'))

        layout_form = QHBoxLayout()
        layout_form.addStretch()
        layout_form.addWidget(contain_form)
        layout_form.addStretch()

        self.setLayout(layout_form)

class PlusButton(PopupButton):
    def __init__(self, ascendent, popup_class=Popup):
        super(PlusButton, self).__init__(ascendent=ascendent, popup_class=popup_class)
        map_plus = QPixmap('assets/icons/plus.png')
        self.setIcon(QIcon(map_plus))
        self.setIconSize(QSize(int(Style.unit / 20), int(Style.unit / 20)))
        self.setStyleSheet('border: 0px; margin: 0px; padding: 0px;')
