from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

# COLOURS
#   BACKGROUND 36 41 46
#   HEADER 29 33 37

BACKGROUND = QColor(36, 41, 46)  # light
HEADER = QColor(29, 33, 37)  # dark
TEXT = QColor(25, 25, 25)  # white

palette = QPalette()
palette.setColor(QPalette.Window, BACKGROUND)
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Base, HEADER)
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, Qt.white)
palette.setColor(QPalette.ToolTipText, Qt.white)
palette.setColor(QPalette.Text, TEXT)
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.white)
palette.setColor(QPalette.BrightText, Qt.red)
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, Qt.black)
