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
    QGraphicsDropShadowEffect
)
from PyQt5.QtGui import (
    QImage,
    QPainter
)
from .component import Component

class StreamView(QWidget):
    def __init__(self, parent=None, location='location', address='address'):
        super(StreamView, self).__init__(parent)
        self.image = None
        self.location = location
        self.address = address
        self.setFixedWidth(Component.unit)
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
        self.setContentsMargins(Component.unit / 4, 0, Component.unit / 4, Component.unit / 4)
        self.setSpacing(Component.unit / 4)
        self.setAlignment(Qt.AlignLeft)

    def set_views(self, views):
        (row, col) = (0, 0)
        for index in range(len(views)):
            if col >= 3:
                row += 1
                col = 0
            lbl_address = QLabel()
            lbl_address.setContentsMargins(0, 0, 0, 0)
            lbl_address.setText(views[index].address)
            lbl_address.setAlignment(Qt.AlignCenter)
            lbl_address.setStyleSheet("font: 12px Corbel, sans-serif; font-weight: 10; background: none; color: white; margin: 0px; padding: 0px;")

            lbl_location = QLabel()
            lbl_location.setContentsMargins(0, 0, 0, 0)
            lbl_location.setText(views[index].location)
            lbl_location.setAlignment(Qt.AlignCenter)
            lbl_location.setStyleSheet("font: 12px Corbel, sans-serif; font-weight: 10; background: none; color: white; margin: 0px; padding: 0px;")

            layout = QVBoxLayout()
            layout.setAlignment(Qt.AlignTop)
            layout.addWidget(views[index])
            # layout.addWidget(lbl_address)
            # layout.addWidget(lbl_location)

            self.addLayout(layout, row, col)
            self.setRowMinimumHeight(row, (Component.unit * 0.6) + int(Component.unit / 8))
            col += 1


class ButtonToggle(QVBoxLayout, Component):
    def __init__(self, ascendent, left_label, right_label):
        super(ButtonToggle, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)

        self.toggle_layout = QHBoxLayout()
        self.toggle_layout.setContentsMargins(0, 0, 0, 0)
        self.toggle_layout.setAlignment(Qt.AlignCenter)

        self.left_button = ButtonSwitch(self, left_label)
        self.left_button.on()
        self.left_button.button.clicked.connect(self.toggle_handler)

        self.right_button = ButtonSwitch(self, right_label)
        self.right_button.off()
        self.right_button.button.clicked.connect(self.toggle_handler)

        left_container = QWidget()
        left_container.setLayout(self.left_button)
        left_container.setStyleSheet('text-align: center; padding-right: 20px; margin-right: 10px; padding-left: 10px;')

        right_container = QWidget()
        right_container.setLayout(self.right_button)
        right_container.setStyleSheet('text-align: center; padding-left: 20px; margin-left: 10px; padding-right: 10px;')

        self.spacer = QVSeperationLine()

        self.toggle_layout.addWidget(left_container)
        # self.toggle_layout.addWidget(self.spacer)
        self.toggle_layout.addWidget(right_container)

        self.contain_toggle = QWidget()
        self.contain_toggle.setLayout(self.toggle_layout)
        self.contain_toggle.setMinimumHeight(Component.unit / 8)

        self.contain_toggle.setMinimumWidth(Component.unit * 0.6)
        self.contain_toggle.setStyleSheet("background-color: #1d2125; margin: 0px; padding: 0px;") 

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

        self.addWidget(self.button)
        self.addWidget(self.marker)
        self.off()

    def draw(self):
        if self.active:
            self.button.setStyleSheet("margin: 0px; padding: 0px; padding-top: 2px; color: #8cbeff;")
            self.marker.setStyleSheet("background-color:#8cbeff;")
        else:
            self.button.setStyleSheet("margin: 0px; padding: 0px; padding-top: 2px; color: white;") 
            self.marker.setStyleSheet("background-color:#1d2125;")
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

    def toggle_handler(self, btn_index):
        for index in range(len(self.buttons)):
            self.buttons[index].setStyleSheet('margin-left: 35px; font: 18px Corbel, sans-serif; font-weight: 15; color: white;')
            self.highlights[index].setStyleSheet('padding-left: 10px; padding-right: 10px; background-color: white;')
        self.buttons[btn_index].setStyleSheet('margin-left: 35px; font: 18px Corbel, sans-serif; font-weight: 15; color: #8cbeff;')
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
