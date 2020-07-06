from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QSizePolicy,
    QLabel,
    QGraphicsDropShadowEffect,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QFormLayout,
    QRadioButton,
    QSpacerItem
)
from PyQt5.QtGui import (
    QImage,
    QPainter,
    QPixmap
)

from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QDir, Qt, QUrl, QSize
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QStatusBar)
from .component import Component
from .styles import (style_light, light_blue, dark_blue)

class StreamView(QWidget):
    def __init__(self, parent=None, location='Outside', address='10.0.0.115'):
        super(StreamView, self).__init__(parent)
        self.image = None
        self.location = location
        self.address = address
        self.setMinimumWidth(Component.unit)
        self.setContentsMargins(0, 5, 0, 5)
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
        self.setSpacing(0)
        self.setAlignment(Qt.AlignCenter)

    def set_views(self, views):
        (row, col) = (0, 0)
        for index in range(len(views)):
            if col >= 3:
                row += 1
                col = 0
            lbl_address = QLabel()
            lbl_address.setContentsMargins(0, 0, 0, 0)
            lbl_address.setText(views[index].address)
            lbl_address.setAlignment(Qt.AlignLeft)
            lbl_address.setStyleSheet("font: 16px Corbel, sans-serif; font-weight: 10; background: none; color: white; margin: 0px; padding: 0px; margin-top: 5px;")

            lbl_location = QLabel()
            lbl_location.setContentsMargins(0, 0, 0, 0)
            lbl_location.setText(views[index].location)
            lbl_location.setAlignment(Qt.AlignLeft)
            lbl_location.setStyleSheet("font: 16px Corbel, sans-serif; font-weight: 10; background: none; color: white; margin: 0px; padding: 0px; margin-top: 5px;")

            outer_layout = QHBoxLayout()
            outer_layout.setAlignment(Qt.AlignCenter)

            inner_layout = QVBoxLayout()
            inner_layout.setAlignment(Qt.AlignCenter)

            layout_address = QHBoxLayout()
            layout_address.setAlignment(Qt.AlignCenter)

            icon = QLabel()
            map_logo = QPixmap("assets/icons/signal_off.png")
            icon.setPixmap(map_logo.scaled(10, 10, Qt.KeepAspectRatio, Qt.FastTransformation))
            icon.setStyleSheet("margin: 0px; padding: 0px; background-color: " + light_blue + ";")

            layout_address.addWidget(icon)
            layout_address.addWidget(lbl_address)

            layout_location = QHBoxLayout()
            layout_location.setAlignment(Qt.AlignCenter)

            icon = QLabel()
            map_logo = QPixmap("assets/icons/signal_off.png")
            icon.setPixmap(map_logo.scaled(10, 10, Qt.KeepAspectRatio, Qt.FastTransformation))
            icon.setStyleSheet("margin: 0px; padding: 0px; background-color: " + light_blue + ";")

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
            
            self.addWidget(layout_container, row, col)
            self.setRowMinimumHeight(row, (Component.unit * 0.6) + int(Component.unit / 8))
            col += 1
        if col >= 3:
            row += 1
            col = 0


class CenterToggle(QWidget, Component):
    def __init__(self, ascendent, left_label, right_label):
        super(CenterToggle, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)

        self.toggle = ButtonToggle(ascendent, left_label, right_label)
        self.toggle.contain_toggle.setMinimumWidth(Component.unit * 0.6)
        self.toggle.left_container.setStyleSheet('text-align: center; padding-right: 10px; padding-left: 10px; border-radius: 20px; margin-right: 35px;')
        self.toggle.right_container.setStyleSheet('text-align: center; padding-right: 10px; padding-left: 10px; border-radius: 20px; margin-left: 35px;')
        self.toggle.contain_toggle.setStyleSheet('background-color: ' + light_blue + '; margin: 0px; padding: 0px;')
        self.toggle.spacer.setStyleSheet('background-color: white; margin: 0px; padding: 0px;')

        self.setLayout(self.toggle)
        self.setStyleSheet('background-color: ' + light_blue + '; border-radius: 20px; margin: 0px; padding: 0px;')


class PanelToggle(QWidget, Component):
    def __init__(self, ascendent, left_label, right_label):
        super(PanelToggle, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)
        self.toggle = ButtonToggle(ascendent, left_label, right_label)

        self.toggle.left_container.setStyleSheet('text-align: center; margin: 0px; padding: 0px;')
        self.toggle.right_container.setStyleSheet('text-align: center; margin: 0px; padding: 0px;')
        self.toggle.contain_toggle.setStyleSheet('background-color: ' + light_blue + '; margin: 0px; padding: 0px;')
        self.toggle.spacer.setStyleSheet('background-color: black; margin: 0px; padding: 0px;')

        self.toggle.contain_toggle.setMinimumWidth(self.width)
        self.toggle.left_container.setMinimumWidth(self.width / 2)
        self.toggle.right_container.setMinimumWidth(self.width / 2)
        self.setMinimumWidth(self.width)
        self.setLayout(self.toggle)
        self.setStyleSheet('background-color: ' + light_blue + '; margin: 0px; padding: 0px;')


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
        self.contain_toggle.setMinimumHeight(Component.unit / 8)

        self.setAlignment(Qt.AlignCenter)
        self.addWidget(self.contain_toggle)

    def toggle_handler(self):
        self.left_button.toggle()
        self.right_button.toggle()


class ButtonSwitch(QVBoxLayout, Component):
    def __init__(self, ascendent, label):
        super(ButtonSwitch, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)
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
            self.button.setStyleSheet("margin: 0px; padding: 0px; padding-top: 2px; color: #8cbeff;")
            self.marker.setStyleSheet("background-color:#8cbeff; margin: 0px; padding: 0px;")
        else:
            self.button.setStyleSheet("margin: 0px; padding: 0px; padding-top: 2px; color: white;")
            self.marker.setStyleSheet("background-color:" + dark_blue + "; margin: 0px; padding: 0px;")
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

    def addButton(self, label):
        btn = QPushButton()
        btn.setText(label)
        btn.setFixedHeight(Component.unit / 4 * 0.8)
        btn.setMinimumWidth(self.width * 0.9)

        seperator = QHSeperationLine()

        self.buttons.append(btn)
        self.highlights.append(seperator)
        btn.clicked.connect(lambda: self.toggle_handler(self.buttons.index(btn)))

        self.addWidget(btn)
        self.addWidget(seperator)

        self.toggle_handler(0)

    def addPlus(self):
        self.buttons.append(PlusButton(self))
        self.highlights.append(None)

    def toggle_handler(self, btn_index):
        for index in range(len(self.buttons)):
            self.buttons[index].setStyleSheet('margin-left: 35px; font: 18px Corbel, sans-serif; font-weight: 15; color: white;')
            if self.highlights[index] is not None:
                self.highlights[index].setStyleSheet('padding-left: 10px; padding-right: 10px; background-color: ' + dark_blue + ';')
        self.buttons[btn_index].setStyleSheet('margin-left: 35px; font: 18px Corbel, sans-serif; font-weight: 15; color: #8cbeff;')
        if self.highlights[index] is not None:
            self.highlights[btn_index].setStyleSheet('padding-left: 10px; padding-right: 10px; background-color: #8cbeff;')


class QHSeperationLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:white;")
        self.setMinimumWidth(1)
        self.setFixedHeight(1)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)


class QVSeperationLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:white;")
        self.setFixedWidth(1)
        self.setMinimumHeight(1)
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)


class PlusButton(QPushButton, Component):
    def __init__(self, ascendent):
        super(PlusButton, self).__init__(ascendent=ascendent)
        map_plus = QPixmap("assets/icons/plus.png")
        self.setIcon(QIcon(map_plus))
        self.setIconSize(QSize(int(Component.unit / 4), int(Component.unit / 4)))

class PopupButton(QPushButton, Component):
    def __init__(self, ascendent):
        super(PopupButton, self).__init__(ascendent=ascendent)
        self.clicked.connect(self.buildPopup)
        self.popup = Popup(ascendent=self)

    def buildPopup(self):
        self.popup.show()

class Popup(QWidget, Component):
    def __init__(self, ascendent):
        super(Popup, self).__init__(ascendent=ascendent)
        self.setWindowFlags(Qt.WindowFlags(Qt.FramelessWindowHint))
        self.setStyleSheet(style_light)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setGeometry(int((5 * Component.unit) / 2) + int(Component.unit * 2), int(self.height / 2) + int(Component.unit * 2), int(Component.unit * 2), int(Component.unit * 2))

        vbox = QVBoxLayout()
        vbox.addWidget(QLineEdit())
        vbox.addWidget(QLineEdit())

        hbox = QHBoxLayout()
        hbox.addWidget(QRadioButton("Broadcast"))
        hbox.addWidget(QRadioButton("Network"))
        hbox.addWidget(QRadioButton("Off"))
        hbox.addStretch()

        self.btn_submit = QPushButton("Submit")
        self.btn_cancel = QPushButton("Cancel")

        self.btn_submit.setFixedWidth(int(Component.unit / 3))
        self.btn_cancel.setFixedWidth(int(Component.unit / 3))
        self.btn_submit.clicked.connect(self.submit)
        self.btn_cancel.clicked.connect(self.cancel)

        hbox_click = QHBoxLayout()
        hbox_click.addWidget(self.btn_submit)
        hbox_click.addWidget(self.btn_cancel)
        hbox_click.addStretch()

        self.lbl_location = QLabel("Location")
        self.lbl_address = QLabel("Address")
        self.lbl_streaming = QLabel("Streaming")
        self.lbl_empty = QLabel()

        self.lbl_location.setStyleSheet('border: 0px solid white;')
        self.lbl_address.setStyleSheet('border: 0px solid white;')
        self.lbl_streaming.setStyleSheet('border: 0px solid white;')
        self.lbl_empty.setStyleSheet('border: 0px solid white;')

        self.layout = QFormLayout()
        self.layout.setAlignment(Qt.AlignRight)
        self.layout.addRow(self.lbl_location, QLineEdit("Home"))
        self.layout.addRow(self.lbl_address, vbox)
        self.layout.addRow(self.lbl_streaming, hbox)
        self.layout.addRow(self.lbl_empty, hbox_click)

        layout_center = QVBoxLayout()
        layout_center.setAlignment(Qt.AlignCenter)
        layout_center.addLayout(self.layout)
        
        contain_form = QWidget()
        contain_form.setLayout(layout_center)
        contain_form.setMinimumHeight(int(Component.unit * 2))
        contain_form.setStyleSheet("margin: 15px; \
                                    padding: 15px; \
                                    border: 2px solid white; \
                                    border-radius: 15px; \
                                    background-color: " + light_blue + "; \
                                    color: white; \
                                    font: 18px Corbel, sans-serif; \
                                    font-weight: 30;")

        layout_form = QHBoxLayout()
        layout_form.addStretch()
        layout_form.addWidget(contain_form)
        layout_form.addStretch()

        self.setLayout(layout_form)

    def submit(self):
        self.hide()

    def cancel(self):
        self.hide()
