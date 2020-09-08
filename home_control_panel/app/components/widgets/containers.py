import cv2
import time
import threading
from cv2 import resize
from PyQt5.QtCore import (
    Qt,
    QPoint
)
from PyQt5.QtGui import (
    QImage,
    QPixmap,
    QPainter
)
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QGraphicsDropShadowEffect
)
from .spacers import QHSeperationLine
from ..component import Component
from ..style import Style
from .buttons import (
    ListButton,
    PlusButton,
    PlayButton,
    PlayToggleButton
)
from ..popups import (
    LocationPopup,
    CameraPopup
)


class LabelList(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(LabelList, self).__init__(ascendent=ascendent)
        self.setAlignment(Qt.AlignTop)
        self.labels = []

    def set_labels(self, labels):
        for label in labels:
            self.add_label(label)

    def add_label(self, label):
        seperator = QHSeperationLine()

        lbl = QLabel(label)
        lbl.setFixedHeight(Style.unit / 4 * 0.8)
        lbl.setMinimumWidth(self.width * 0.9)

        lbl.setStyleSheet(Style.replace_variables('margin: 0px; \
                                font: @ButtonTextSize @TextFont; \
                                font-weight: 15; \
                                color: @LightTextColor;'))

        seperator.setStyleSheet(Style.replace_variables('padding-left: @MediumPadding; \
                                padding-right: @MediumPadding; \
                                background-color: @DarkColor;'))
        self.labels.append(lbl)

        lbl_container = QVBoxLayout()
        lbl_container.addWidget(lbl)
        lbl_container.addWidget(seperator)

        lbl_widget = QWidget()
        lbl_widget.setLayout(lbl_container)
        lbl_widget.setStyleSheet(Style.replace_variables('border: 0px; border-radius: @LargeRadius;'))

        self.addWidget(lbl_widget)

    def clear_labels(self):
        for i in reversed(range(self.count())):
            self.itemAt(i).widget().deleteLater()


class ButtonList(QVBoxLayout, Component):
    def __init__(self, ascendent):
        super(ButtonList, self).__init__(ascendent=ascendent)
        self.setAlignment(Qt.AlignTop)
        self.buttons = {}
        self.highlights = {}
        self.active_index = ''
        self.append_plus()

    def add_button(self, label):
        seperator = QHSeperationLine()

        if len(self.buttons) > 0:
            self.removeWidget(self.buttons[''])
            self.buttons[''].deleteLater()
            del self.buttons['']

        btn = ListButton(label, self)
        btn.setText(label)
        btn.setFixedHeight(Style.unit / 4 * 0.8)
        btn.setMinimumWidth(self.width * 0.9)

        btn.setStyleSheet(Style.replace_variables('margin-left: @LargeMargin; \
                                font: @ButtonTextSize @TextFont; \
                                font-weight: 15; \
                                color: @LightTextColor;'))
        seperator.setStyleSheet(Style.replace_variables('padding-left: @MediumPadding; \
                                padding-right: @MediumPadding; \
                                background-color: @DarkColor;'))

        self.buttons[label] = btn
        self.highlights[label] = seperator

        self.addWidget(btn)
        self.addWidget(seperator)
        self.append_plus()
        self.toggle_handler(label)

    def append_plus(self):
        btn = PlusButton(self, LocationPopup)
        btn_holder = QHBoxLayout()
        btn_container = QWidget()
        inner_layout = QHBoxLayout()
        outer_layout = QVBoxLayout()
        layout_container = QWidget()

        btn.setContentsMargins(0, 0, 0, 0)

        btn_holder.setAlignment(Qt.AlignCenter)
        btn_holder.addStretch()
        btn_holder.addWidget(btn)
        btn_holder.addStretch()
        btn_holder.setContentsMargins(0, 0, 0, 0)
        btn_holder.setSpacing(0)

        btn_container.setLayout(btn_holder)

        inner_layout.setAlignment(Qt.AlignCenter)
        inner_layout.addWidget(btn_container)

        outer_layout.setAlignment(Qt.AlignCenter)
        outer_layout.addLayout(inner_layout)

        layout_container.setLayout(outer_layout)
        layout_container.setStyleSheet(Style.replace_variables('margin: @None; padding-top: @PaddingMedium;'))

        self.buttons[''] = layout_container
        self.addWidget(layout_container)

    def toggle_handler(self, btn_index):
        if len(self.buttons) > 0:
            self.buttons[self.active_index].setStyleSheet(Style.replace_variables('margin-left: @LargeMargin; \
                                                            font: @ButtonTextSize @TextFont; \
                                                            font-weight: 15; \
                                                            color: @LightTextColor;'))
            if self.active_index in self.highlights and self.highlights[self.active_index] is not None:
                self.highlights[self.active_index].setStyleSheet(Style.replace_variables('padding-left: @MediumPadding; \
                                                            padding-right: @MediumPadding; \
                                                            background-color: @DarkColor;'))
            if btn_index in self.buttons:
                self.buttons[btn_index].setStyleSheet(Style.replace_variables('margin-left: @LargeMargin; \
                                                                font: @ButtonTextSize @TextFont; \
                                                                font-weight: 15; \
                                                                color: @HighlightTextColor;'))
                if self.highlights[btn_index] is not None:
                    self.highlights[btn_index].setStyleSheet(Style.replace_variables('padding-left: @MediumPadding; \
                                                                padding-right: @MediumPadding; \
                                                                background-color: @HighlightColor;'))
                self.active_index = btn_index

    def clear_buttons(self):
        for i in reversed(range(self.count())): 
            self.itemAt(i).widget().deleteLater()


class StreamView(QWidget):
    def __init__(self, camera, parent=None):
        super(StreamView, self).__init__(parent)
        self.playing = True
        self.qp = QPainter()
        self.image = QImage()
        self.camera = camera
        self.location = camera.location
        self.address = camera.address
        self.dimensions = (int(Style.unit), int(Style.unit * 0.6))
        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumWidth(Style.unit)
        self.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))

        # self.setContextMenuPolicy(Qt.ActionsContextMenu)
        # quitAction = QAction("Remove", self)
        # quitAction.triggered.connect(qApp.quit)
        # self.addAction(quitAction)

    def set_frame(self):
        if self.camera.stream.current_frame is not None:
            frame = resize(self.camera.stream.current_frame, self.dimensions)
            height, width, bpc = frame.shape
            bpl = bpc * width
            self.image = QImage(frame.data, width, height, bpl, QImage.Format_RGB888)
            self.setFixedSize(self.image.size())
            self.update()

    def paintEvent(self, event):
        try:
            self.qp.begin(self)
            if self.image:
                self.qp.drawImage(QPoint(0, 0), self.image)
            self.qp.end()
        except Exception:
            return


class StreamGrid(QGridLayout, Component):
    def __init__(self, ascendent):
        super(StreamGrid, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
        self.setAlignment(Qt.AlignLeft)
        (self.row, self.col) = (0, 0)
        self.views = []
        self.streams = []

    def refresh(self):
        for index in range(len(self.streams)):
            if self.streams[index].playing:
                self.streams[index].set_frame()

    def append_plus(self):
        if self.col >= 3:
            self.row += 1
            self.col = 0
        elif self.col < 0:
            self.row -= max(1, 0)
            self.col = max(2, 0)

        btn = PlusButton(self, CameraPopup)
        btn.setStyleSheet('border: @None; margin: @None; padding: @None;')
        btn.setContentsMargins(0, 0, 0, 0)
        btn_holder = QVBoxLayout()
        btn_holder.setAlignment(Qt.AlignCenter)
        btn_holder.addWidget(btn)

        btn_container_in = QWidget()
        btn_container_in.setContentsMargins(0, 0, 0, 0)
        btn_container_in.setLayout(btn_holder)
        btn_container_in.setFixedWidth(Style.unit * 0.7)
        btn_container_in.setFixedHeight(Style.unit * 0.5)
        btn_container_in.setStyleSheet(Style.replace_variables('border: @None; \
                                                            margin: @None; \
                                                            padding: @None;'))
        btn_holder_out = QHBoxLayout()
        btn_holder_out.setContentsMargins(0, 0, 0, 0)
        btn_holder_out.setSpacing(0)
        btn_holder_out.setAlignment(Qt.AlignCenter)
        btn_holder_out.addStretch()
        btn_holder_out.addWidget(btn_container_in)
        btn_holder_out.addStretch()

        btn_container = QWidget()
        btn_container.setContentsMargins(0, 0, 0, 0)
        btn_container.setLayout(btn_holder_out)
        btn_container.setFixedWidth(Style.unit * 0.8)
        btn_container.setFixedHeight(Style.unit * 0.6)
        btn_container.setStyleSheet(Style.replace_variables('border: @BorderThin solid @LightTextColor; \
                                                            margin: @None; \
                                                            padding: @None;'))
        btn_container.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))

        inner_layout = QHBoxLayout()
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.setSpacing(0)
        inner_layout.setAlignment(Qt.AlignCenter)
        inner_layout.addWidget(btn_container)

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        outer_layout.setAlignment(Qt.AlignTop)
        outer_layout.addLayout(inner_layout)

        centre_layout = QVBoxLayout()
        centre_layout.setContentsMargins(0, 0, 0, 0)
        centre_layout.setSpacing(0)
        centre_layout.setAlignment(Qt.AlignLeft)
        centre_layout.addLayout(outer_layout)

        layout_container = QWidget()
        layout_container.setContentsMargins(0, 0, 0, 0)
        layout_container.setLayout(centre_layout)
        layout_container.setMaximumWidth(Style.unit + int(Style.unit / 4))
        layout_container.setStyleSheet(Style.replace_variables('border: @None; \
                                                                margin: @None; \
                                                                padding: @None;'))
        self.addWidget(layout_container, self.row, self.col)
        self.setRowMinimumHeight(self.row, (Style.unit * 0.6) + int(Style.unit / 8))

        self.views.append(layout_container)
        self.col += 1

        self.update()

    def add_view(self, camera, append=True):
        if append and len(self.views) > 0:
            self.remove_view(len(self.views) - 1)

        if self.col >= 3:
            self.row += 1
            self.col = 0
        elif self.col < 0:
            self.row -= max(1, 0)
            self.col = max(2, 0)

        view = StreamView(camera)
        self.streams.append(view)

        lbl_address = QLabel()
        lbl_address.setContentsMargins(0, 0, 0, 0)
        lbl_address.setText(view.address)
        lbl_address.setAlignment(Qt.AlignCenter)
        lbl_address.setStyleSheet(Style.replace_variables('font: @SmallTextSize @TextFont; \
                                                            font-weight: 10; \
                                                            background: none; \
                                                            color: @LightTextColor; \
                                                            margin: @None; \
                                                            padding: @None; \
                                                            margin-top: @MarginSmall;'))
        lbl_location = QLabel()
        lbl_location.setContentsMargins(0, 0, 0, 0)
        lbl_location.setText(view.location)
        lbl_location.setAlignment(Qt.AlignCenter)
        lbl_location.setStyleSheet(Style.replace_variables('font: @SmallTextSize @TextFont; \
                                                            font-weight: 10; \
                                                            background: none; \
                                                            color: @LightTextColor; \
                                                            margin: @None; \
                                                            padding: @None; \
                                                            margin-top: @MarginSmall;'))
        outer_layout = QHBoxLayout()
        outer_layout.setAlignment(Qt.AlignCenter)
        inner_layout = QVBoxLayout()
        inner_layout.setAlignment(Qt.AlignCenter)

        layout_address = QHBoxLayout()
        layout_address.setAlignment(Qt.AlignLeft)
        layout_location = QHBoxLayout()
        layout_location.setAlignment(Qt.AlignLeft)

        icon = QLabel()
        map_logo = QPixmap('assets/icons/signal_off.png')
        icon.setPixmap(map_logo.scaled(10, 10, Qt.KeepAspectRatio, Qt.FastTransformation))
        icon.setStyleSheet(Style.replace_variables('margin: @None; \
                                                    padding: @None; \
                                                    background-color: transparent;'))
        layout_address.addWidget(icon)
        layout_address.addWidget(lbl_address)

        icon = QLabel()
        map_logo = QPixmap('assets/icons/signal_off.png')
        icon.setPixmap(map_logo.scaled(10, 10, Qt.KeepAspectRatio, Qt.FastTransformation))
        icon.setStyleSheet(Style.replace_variables('margin: @None; \
                                                    padding: @None; \
                                                    background-color: transparent;'))
        layout_location.addWidget(icon)
        layout_location.addWidget(lbl_location)

        info_layout = QVBoxLayout()
        info_layout.addLayout(layout_address)
        info_layout.addLayout(layout_location)

        control_layout = QHBoxLayout()
        control_layout.addLayout(info_layout)
        control_layout.addWidget(PlayToggleButton(view))

        info_widget = QWidget()
        info_widget.setLayout(control_layout)
        info_widget.setContentsMargins(int(Style.unit / 8), Style.sizes.margin_small, 0, 0)

        inner_layout.addWidget(view)
        inner_layout.addWidget(info_widget)

        outer_layout.addStretch()
        outer_layout.addLayout(inner_layout)
        outer_layout.addStretch()

        layout_container = QWidget()
        layout_container.setMaximumWidth(Style.unit + int(Style.unit / 4))
        layout_container.setLayout(outer_layout)
        self.addWidget(layout_container, self.row, self.col)
        self.setRowMinimumHeight(self.row, (Style.unit * 0.6) + int(Style.unit / 8))
        self.views.append(layout_container)

        if append:
            self.append_plus()

        self.col += 1

        self.update()

    def remove_view(self, index):
        if self.col >= 3:
            self.row += 1
            self.col = 0
        elif self.col < 0:
            self.row -= 1
            self.col = 2
        if 0 <= index and index < len(self.streams) and self.streams[index] is not None:
            del self.streams[index]
        if 0 <= index and index < len(self.views) and self.views[index] is not None:
            self.removeWidget(self.views[index])
            self.views[index].deleteLater()
            del self.views[index]
            self.col -= 1

    def clear_views(self):
        while len(self.views) > 0:
            self.remove_view(0)
        (self.row, self.col) = (0, 0)
        self.views = []

    def add_views(self, cameras):
        for index in range(len(cameras)):
            self.add_view(cameras[index], False)
        self.append_plus()

    def reset(self, cameras):
        self.clear_views()
        self.add_views(cameras)
        self.update()


class Player(threading.Thread):
    def __init__(self, filepath, view):
        threading.Thread.__init__(self)
        self.connection = None
        self.current_frame = None
        self.filepath = filepath
        self.view = view
        self.started = False
        self.playing = False

    def run(self):
        self.started = True
        self.connection = cv2.VideoCapture(self.filepath)
        self.playing = True
        while self.connection.isOpened():
            (grabbed, frame) = self.connection.read()
            if grabbed:
                self.current_frame = frame
                self.view.set_frame(self.current_frame)
                time.sleep(1/60)
            else:
                break
        self.playing = False
        self.connection.release()

    def stop(self):
        self.connection.release()
        self.playing = False

class VideoView(QWidget):
    def __init__(self, filepath, parent=None):
        super(VideoView, self).__init__(parent)
        self.dimensions = (int(Style.unit), int(Style.unit * 0.6))
        self.player = None
        self.filepath = filepath
        self.qp = QPainter()
        self.image = QImage()
        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumWidth(Style.unit)
        self.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))

    def play(self):
        if self.player is None:
            self.player = Player(self.filepath, self)

        if self.player.started:
            if not self.player.playing:
                self.player.join()
                self.player = None
                self.play()
            else:
                self.player.stop()
        else:
            self.player.start()

    def set_frame(self, current_frame):
        if current_frame is not None:
            frame = resize(current_frame, self.dimensions)
            height, width, bpc = frame.shape
            bpl = bpc * width
            self.image = QImage(frame.data, width, height, bpl, QImage.Format_RGB888)
            self.setFixedSize(self.image.size())
            self.update()

    def paintEvent(self, event):
        try:
            self.qp.begin(self)
            if self.image:
                self.qp.drawImage(QPoint(0, 0), self.image)
            self.qp.end()
        except Exception:
            return


class VideoGrid(QGridLayout, Component):
    def __init__(self, ascendent):
        super(VideoGrid, self).__init__(ascendent=ascendent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
        self.setAlignment(Qt.AlignLeft)
        (self.row, self.col) = (0, 0)
        self.views = []
        self.streams = []
        self.paths = []

    def add_view(self, path):
        if path in self.paths:
            return

        if self.col >= 3:
            self.row += 1
            self.col = 0
        elif self.col < 0:
            self.row -= max(1, 0)
            self.col = max(2, 0)

        view = VideoView(path)
        self.streams.append(view)
        self.paths.append(path)

        outer_layout = QHBoxLayout()
        outer_layout.setAlignment(Qt.AlignCenter)

        inner_layout = QVBoxLayout()
        inner_layout.setAlignment(Qt.AlignCenter)

        inner_layout.addWidget(view)
        inner_layout.addWidget(PlayButton(view))

        outer_layout.addStretch()
        outer_layout.addLayout(inner_layout)
        outer_layout.addStretch()

        layout_container = QWidget()
        layout_container.setMaximumWidth(Style.unit + int(Style.unit / 4))
        layout_container.setLayout(outer_layout)
        self.addWidget(layout_container, self.row, self.col)
        self.setRowMinimumHeight(self.row, (Style.unit * 0.6) + int(Style.unit / 8))

        self.col += 1

        view.play()

        self.update()

    def clear_views(self):
        for i in reversed(range(self.count())): 
            self.itemAt(i).widget().deleteLater()
        (self.row, self.col) = (0, 0)
        self.streams = []

    def add_views(self, cameras):
        for index in range(len(cameras)):
            self.add_view(cameras[index], False)
        self.append_plus()

    def reset(self, cameras):
        self.clear_views()
        self.add_views(cameras)
        self.update()
