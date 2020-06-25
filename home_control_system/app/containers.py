from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QDesktopWidget
)
from .widgets import StreamView


###############################
# LAYOUT CONTAINER
#   - Side Panel
#   - View Panel
class Layout(QHBoxLayout):
    def __init__(self, *args, **kwargs):
        super(Layout, self).__init__(*args, **kwargs)
        
        self.sidepanel = SidePanel()
        self.view = ViewPanel()

        self.addLayout(self.sidepanel, 1)
        self.addLayout(self.view, 5)

    def add_cameras(self, cameras):
        self.view.stream_grid.set_stream_views(cameras)
###############################


###############################
# SIDE PANEL CONTAINER
#   - Location
#   - Rooms/Alerts List
class SidePanel(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(SidePanel, self).__init__(*args, **kwargs)
###############################


###############################
# VIEW PANEL CONTAINER
#   - Header Block
#   - Stream Grid
class ViewPanel(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(ViewPanel, self).__init__(*args, **kwargs)
        self.stream_grid = StreamGrid()
        self.addLayout(self.stream_grid)


class StreamGrid(QGridLayout):
    def __init__(self, *args, **kwargs):
        super(StreamGrid, self).__init__(*args, **kwargs)
        sizeObject = QDesktopWidget().screenGeometry(-1)
        self.width = sizeObject.width() / 2
        self.height = sizeObject.height() / 1.66

    def set_stream_views(self, cameras):
        for index in range(len(cameras)):
            cameras[index].set_stream_dimensions(self.height / len(cameras), self.width / len(cameras))
            cameras[index].set_stream_view(StreamView())
        (row, col) = (0, 0)
        for index in range(len(cameras)):
            if col == 2:
                row += 1
                col = 0
            self.addWidget(cameras[index].get_stream_view(), row, col)
            col += 1
###############################
