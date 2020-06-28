from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QHBoxLayout
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
        # self.set_dimensions(self.width, (self.height / 26) * 23)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

    def set_views(self, views):
        (row, col) = (0, 0)
        for index in range(len(views)):
            if col == 0:
                views[index].setContentsMargins(int(Component.unit / 8), 0, int(Component.unit / 4), int(Component.unit / 8))
            elif col == 1:
                views[index].setContentsMargins(0, 0, int(Component.unit / 4), int(Component.unit / 8))
            elif col == 2:
                views[index].setContentsMargins(0, 0, int(Component.unit / 4), int(Component.unit / 8))
            elif col >= 3:
                views[index].setContentsMargins(0, 0, int(Component.unit / 8), int(Component.unit / 8))
                row += 1
                col = 0
            self.addWidget(views[index], row, col)
            self.setRowMinimumHeight(row, (Component.unit * 0.6) + int(Component.unit / 8))
            col += 1


class ButtonToggle(QHBoxLayout, Component):
    def __init__(self):
        super(ButtonToggle, self).__init__()


class ButtonList(QHBoxLayout, Component):
    def __init__(self):
        super(ButtonList, self).__init__()
