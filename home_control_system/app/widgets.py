from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import (
    QImage,
    QPainter,
    QPalette,
    QColor
)


class Color(QWidget):
    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class StreamView(QWidget):
    def __init__(self, parent=None):
        super(StreamView, self).__init__(parent)
        self.image = None

    def setFrame(self, frame):
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