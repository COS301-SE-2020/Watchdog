from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QScrollArea
)
from PyQt5.QtCore import Qt
from .component import Component
from .widgets import StreamView


###############################
# LAYOUT CONTAINER
#   - Side Panel
#   - View Panel
class MainLayout(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(MainLayout, self).__init__(ascendent=ascendent)
        spacer = QSpacerItem(5, self.width, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.sidepanel = SidePanel(self)
        self.view = ViewPanel(self)
        layout = QHBoxLayout()
        layout.addLayout(self.sidepanel, 1)
        layout.addLayout(self.view, 5)
        self.addSpacerItem(spacer)
        self.addLayout(layout)

    def add_cameras(self, cameras):
        self.view.stream_grid.set_stream_views(cameras)
###############################


###############################
# SIDE PANEL CONTAINER
#   - Location
#   - Rooms/Alerts List
class SidePanel(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(SidePanel, self).__init__(ascendent=ascendent)

###############################


###############################
# VIEW PANEL CONTAINER
#   - Header Block
#   - Stream Grid
class ViewPanel(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(ViewPanel, self).__init__(ascendent=ascendent)

        self.stream_grid = StreamGrid(self)

        # widget = QWidget()                 # Widget that contains the collection of Vertical Box
        # widget.setLayout(self.stream_grid)
        # # Scroll Area Properties
        # self.scroll = QScrollArea()
        # self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.scroll.setWidgetResizable(True)
        # self.scroll.setWidget(widget)

        self.addLayout(self.stream_grid)

class StreamGrid(QGridLayout, Component):
    def __init__(self, ascendent):
        super(StreamGrid, self).__init__(ascendent=ascendent)

    def set_stream_views(self, cameras):
        views = []
        for index in range(len(cameras)):
            view = StreamView()
            cameras[index].init_stream(view, self.width / 3, self.height / len(cameras))
            views.append(view)
        (row, col) = (0, 0)
        for index in range(len(views)):
            if col > 2:
                row += 1
                col = 0
            self.addWidget(views[index], row, col)
            col += 1
###############################
