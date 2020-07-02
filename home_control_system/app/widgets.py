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
    QGraphicsDropShadowEffect
)
from PyQt5.QtGui import (
    QImage,
    QPainter
)
from .component import Component

class StreamView(QWidget):
    def __init__(self, parent=None):
        super(StreamView, self).__init__(parent)
        self.image = None
        self.setFixedWidth(Component.unit)
        self.setContentsMargins(0, 0, 0, 0)
        shadow = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        self.setGraphicsEffect(shadow)

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

    def set_views(self, views):
        (row, col) = (0, 0)
        for index in range(len(views)):
            if col >= 3:
                row += 1
                col = 0
            layout = QHBoxLayout()
            layout.setAlignment(Qt.AlignCenter)
            layout.addWidget(views[index])
            self.addLayout(layout, row, col)
            self.setRowMinimumHeight(row, (Component.unit * 0.6) + int(Component.unit / 8))
            col += 1


class ButtonToggle(QVBoxLayout, Component):
    def __init__(self, ascendent, left_label, right_label):
        super(ButtonToggle, self).__init__(ascendent=ascendent)

        self.toggle_layout = QHBoxLayout()
        self.toggle_layout.setContentsMargins(0, 0, 0, 0)
        self.toggle_layout.setAlignment(Qt.AlignCenter)

        self.left_button = ButtonSwitch(self, left_label)
        self.left_button.on()
        self.left_button.button.clicked.connect(self.toggle_handler)

        self.spacer = QVSeperationLine()
        self.right_button = ButtonSwitch(self, right_label)
        self.right_button.button.clicked.connect(self.toggle_handler)

        left_container = QWidget()
        left_container.setLayout(self.left_button)
        left_container.setMaximumWidth(Component.unit / 2)
        left_container.setStyleSheet('text-align: center; padding-bottom: 2px;')


        right_container = QWidget()
        right_container.setLayout(self.right_button)
        right_container.setMaximumWidth(Component.unit / 2)
        right_container.setStyleSheet('text-align: center; padding-bottom: 2px;')


        self.toggle_layout.addWidget(left_container)
        self.toggle_layout.addWidget(self.spacer)
        self.toggle_layout.addWidget(right_container)

        self.contain_toggle = QWidget()
        self.contain_toggle.setLayout(self.toggle_layout)
        self.contain_toggle.setMinimumHeight(Component.unit / 8)

        self.contain_toggle.setMinimumWidth(Component.unit)
        self.contain_toggle.setStyleSheet("background-color: #1d2125;") 

        shadow = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        self.contain_toggle.setGraphicsEffect(shadow)

        self.setAlignment(Qt.AlignCenter)
        self.addWidget(self.contain_toggle)

    def toggle_handler(self):
        print("Handled")
        self.left_button.toggle()
        self.right_button.toggle()

class ButtonSwitch(QVBoxLayout, Component):
    def __init__(self, ascendent, label):
        super(ButtonSwitch, self).__init__(ascendent=ascendent)
        self.active = False
        self.marker = QHSeperationLine()
        self.marker.setStyleSheet("background-color:#1d2125;")

        self.button = QPushButton()
        self.button.setText(label)
        self.button.setMinimumHeight(25)
        self.addWidget(self.button)
        self.addWidget(self.marker)

        self.draw()

    def draw(self):
        if self.active:
            self.marker.setStyleSheet("background-color:white;")
        else:
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
        self.setAlignment(Qt.AlignLeft)
        self.buttons = []

    def addButton(self, label):
        btn = QPushButton()
        btn.setText(label)
        btn.setFixedHeight(Component.unit / 4)
        btn.setMinimumWidth(self.width * 0.9)
        btn.setStyleSheet('margin-left: 25px; font: 18px Corbel, sans-serif;')
        self.buttons.append(btn)

        seperator = QHSeperationLine()
        self.addWidget(btn)
        self.addWidget(seperator)


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
