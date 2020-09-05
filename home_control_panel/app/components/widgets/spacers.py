from PyQt5.QtWidgets import (
    QFrame,
    QSizePolicy
)
from ..style import Style


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
