from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
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
            # if col == 0:
                # views[index].setContentsMargins(int(Component.unit / 8), 0, int(Component.unit / 4), int(Component.unit / 8))
            # elif col == 1:
                # views[index].setContentsMargins(0, 0, int(Component.unit / 4), int(Component.unit / 8))
            # elif col == 2:
                # views[index].setContentsMargins(0, 0, int(Component.unit / 4), int(Component.unit / 8))
            if col >= 3:
                # views[index].setContentsMargins(0, 0, 0, int(Component.unit / 8))
                row += 1
                col = 0
            self.addWidget(views[index], row, col)
            self.setRowMinimumHeight(row, (Component.unit * 0.6) + int(Component.unit / 8))
            col += 1


class ButtonToggle(QHBoxLayout, Component):
    def __init__(self, ascendent, left_label, right_label):
        super(ButtonToggle, self).__init__(ascendent=ascendent)

        self.setContentsMargins(0, 0, 0, 0)
        self.setAlignment(Qt.AlignCenter)

        self.left_button = QPushButton()
        self.left_button.setText(left_label)

        self.spacer = QLabel()
        self.spacer.setText('|')
        self.spacer.setStyleSheet("QLabel {                             \
                                        font: 26px Corbel, sans-serif;  \
                                    }")                                 

        self.right_button = QPushButton()
        self.right_button.setText(right_label)

        self.left_button.setContentsMargins(0, 0, 0, 0)
        self.spacer.setContentsMargins(5, 0, 5, 0)
        self.right_button.setContentsMargins(0, 0, 0, 0)

        self.addWidget(self.left_button)
        self.addWidget(self.spacer)
        self.addWidget(self.right_button)

class ButtonList(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(ButtonList, self).__init__(ascendent=ascendent)
        self.setAlignment(Qt.AlignLeft)
        self.buttons = []

    def addButton(self, label):
        btn = QPushButton()
        btn.setMinimumHeight(Component.unit / 4)
        btn.setMinimumWidth(self.width * 0.9)
        btn.setContentsMargins((Component.unit / 4), (Component.unit / 8), 0, (Component.unit / 8))
        btn.setText(label)
        self.buttons.append(btn)
        self.addWidget(btn)
