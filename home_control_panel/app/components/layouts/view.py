from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QGraphicsDropShadowEffect
)
from ..style import Style
from ..component import Component
from ..widgets.buttons import CenterToggle
from ..widgets.containers import (
    StreamGrid,
    VideoGrid
)

###############################
# VIEW PANEL CONTAINER
#   - Header Block [CONTAINER]
#   - Stream Grid [CONTAINER]
class View(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(View, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width * 4/5, self.height * 1/8)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        self.grid = GridLayout(self)

        # # Light View
        contain_grid = QWidget()
        contain_grid.setContentsMargins(0, 0, 0, 0)
        contain_grid.setLayout(self.grid)
        contain_grid.setStyleSheet(Style.light)
        contain_grid.setMinimumWidth(self.width)

        self.addWidget(contain_grid)
# VIEW GRID CONTAINER
#   - Stream Views [WIDGET]
class GridLayout(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(GridLayout, self).__init__(ascendent=ascendent)
        self.set_dimensions(self.width, self.height * 7/8)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
        self.setAlignment(Qt.AlignCenter)

        self.view_toggle = CenterToggle(self, 'Live', 'Clips')

        layout_above = QVBoxLayout()
        layout_above.setAlignment(Qt.AlignCenter)
        layout_above.setContentsMargins(0, 0, 0, 0)
        layout_above.setSpacing(0)
        layout_above.addStretch(12)
        layout_above.addWidget(self.view_toggle)

        widget_above = QWidget()
        widget_above.setLayout(layout_above)
        widget_above.setContentsMargins(0, 0, 0, 0)
        widget_above.setFixedHeight(Style.unit * 0.32)

        self.viewer = StreamGrid(self)
        self.retriever = VideoGrid(self)

        contain_live = QVBoxLayout()
        contain_live.setContentsMargins(0, 0, 0, 0)
        contain_live.setAlignment(Qt.AlignCenter)
        contain_live.addLayout(self.viewer)
        contain_live.addStretch()

        contain_historical = QVBoxLayout()
        contain_historical.setContentsMargins(0, 0, 0, 0)
        contain_historical.setAlignment(Qt.AlignCenter)
        contain_historical.addLayout(self.retriever)
        contain_historical.addStretch()

        self.live_viewer = QWidget()
        self.live_viewer.setLayout(contain_live)
        self.live_viewer.setFixedWidth(self.width * 0.85)

        self.historical_viewer = QWidget()
        self.historical_viewer.setLayout(contain_historical)
        self.historical_viewer.setFixedWidth(self.width * 0.85)

        info_box = QHBoxLayout()
        info_box.setAlignment(Qt.AlignCenter)
        info_box.addWidget(QLabel('Login to view your content...'))

        self.info_label = QWidget()
        self.info_label.setLayout(info_box)

        contain_both = QHBoxLayout()
        contain_both.setContentsMargins(0, 0, 0, 0)

        contain_both.addWidget(self.live_viewer)
        contain_both.addWidget(self.historical_viewer)
        contain_both.addWidget(self.info_label)

        self.live_view = False
        self.toggle()

        # Widget that contains the collection of Vertical Box
        self.contain_viewer = QWidget()
        self.contain_viewer.setContentsMargins(0, 0, 0, 0)
        self.contain_viewer.setLayout(contain_both)
        self.contain_viewer.setStyleSheet(Style.replace_variables('border: @None; \
                                                                margin @None; \
                                                                padding @None; \
                                                                background-color: @DarkColor;'))
        self.scroll = QScrollArea()
        self.scroll.setContentsMargins(0, 0, 0, 0)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.contain_viewer)
        self.scroll.setMinimumWidth(self.width)

        main_container = QVBoxLayout()
        main_container.setContentsMargins(0, 0, 0, 0)
        main_container.setAlignment(Qt.AlignCenter)
        main_container.addWidget(widget_above)
        main_container.addWidget(self.scroll)

        main_widget = QWidget()
        main_widget.setLayout(main_container)
        main_widget.setStyleSheet(Style.replace_variables('margin: ' + str(Style.sizes.margin_large * 1.4) + 'px; \
                                                            padding: @None; \
                                                            border: none; \
                                                            border-radius: @LargeRadius; \
                                                            background-color: @DarkColor;'))
        main_widget.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=10, xOffset=3, yOffset=3))

        self.addWidget(main_widget)
        self.show()

    def show(self):
        self.info_label.hide()
        self.view_toggle.show()
        if self.live_view:
            self.live_viewer.show()
            self.historical_viewer.hide()
        else:
            self.historical_viewer.show()
            self.live_viewer.hide()
        self.update()

    def hide(self):
        self.info_label.show()
        self.view_toggle.hide()
        self.live_viewer.hide()
        self.historical_viewer.hide()

    def toggle(self):
        if self.live_view:
            self.live_view = False
            self.live_viewer.hide()
            self.historical_viewer.show()
        else:
            self.live_view = True
            self.historical_viewer.hide()
            self.live_viewer.show()
        self.update()

    def set_stream_views(self, cameras):
        self.viewer.reset(cameras)

    def add_stream_view(self, camera):
        self.viewer.add_view(camera)
###############################
