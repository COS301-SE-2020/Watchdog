import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QLineEdit,
    QFormLayout,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QRadioButton
)
from .component import Component
from .style import Style


class PopupButton(QPushButton, Component):
    def __init__(self, ascendent, popup_class):
        super(PopupButton, self).__init__(ascendent=ascendent)
        self.clicked.connect(self.buildPopup)
        self.popup = popup_class(ascendent=self)

    def buildPopup(self):
        self.popup.show()


class Popup(QWidget, Component):
    def __init__(self, ascendent):
        super(Popup, self).__init__(ascendent=ascendent)
        if os.name == 'nt':
            self.setWindowFlags(Qt.WindowFlags(Qt.FramelessWindowHint))
        self.setStyleSheet(Style.replace_variables(Style.light))
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        top_margin = Style.unit * 1.5
        left_margin = Style.unit * 2.5
        main_height = int(3 * Style.unit)
        main_width = int(5 * Style.unit)
        popup_width = int(Style.unit * 2)
        self.setGeometry(left_margin + (main_width / 2) - (popup_width / 2), top_margin + (main_height / 2) - (popup_width / 2), popup_width, popup_width)

    def submit(self):
        self.hide()

    def cancel(self):
        self.hide()


class SettingsPopup(Popup):
    def __init__(self, ascendent):
        super(SettingsPopup, self).__init__(ascendent=ascendent)

        hbox = QHBoxLayout()
        hbox.addWidget(QRadioButton('Broadcast'))
        hbox.addWidget(QRadioButton('Network'))
        hbox.addWidget(QRadioButton('Off'))
        hbox.addStretch()

        self.btn_submit = QPushButton('Submit')
        self.btn_cancel = QPushButton('Cancel')

        self.btn_submit.setFixedWidth(int(Style.unit / 3))
        self.btn_cancel.setFixedWidth(int(Style.unit / 3))
        self.btn_submit.clicked.connect(self.submit)
        self.btn_cancel.clicked.connect(self.cancel)

        hbox_click = QHBoxLayout()
        hbox_click.addWidget(self.btn_submit)
        hbox_click.addWidget(self.btn_cancel)
        hbox_click.addStretch()

        self.lbl_location = QLabel('Location')
        self.lbl_address = QLabel('Address')
        self.lbl_streaming = QLabel('Streaming')
        self.lbl_empty = QLabel()

        self.lbl_location.setStyleSheet(Style.replace_variables('border: @None;'))
        self.lbl_address.setStyleSheet(Style.replace_variables('border: @None;'))
        self.lbl_streaming.setStyleSheet(Style.replace_variables('border: @None;'))
        self.lbl_empty.setStyleSheet(Style.replace_variables('border: @None;'))

        self.input_location = QLineEdit(Component.root.settings.site)
        self.input_address = QLineEdit(Component.root.settings.address)

        self.layout = QFormLayout()
        self.layout.setAlignment(Qt.AlignRight)
        self.layout.addRow(self.lbl_location, self.input_location)
        self.layout.addRow(self.lbl_address, self.input_address)
        self.layout.addRow(self.lbl_streaming, hbox)
        self.layout.addRow(self.lbl_empty, hbox_click)

        layout_center = QVBoxLayout()
        layout_center.setAlignment(Qt.AlignCenter)
        layout_center.addLayout(self.layout)

        contain_form = QWidget()
        contain_form.setLayout(layout_center)
        contain_form.setMinimumHeight(int(Style.unit * 2))
        contain_form.setStyleSheet(Style.replace_variables('margin: @MediumMargin; \
                                                            padding: @LargePadding; \
                                                            border: @BorderThick solid @LightTextColor; \
                                                            border-radius: @SmallRadius; \
                                                            background-color: @LightColor; \
                                                            color: @LightTextColor; \
                                                            font: @ButtonTextSize @TextFont; \
                                                            font-weight: 30;'))
        layout_form = QHBoxLayout()
        layout_form.addStretch()
        layout_form.addWidget(contain_form)
        layout_form.addStretch()

        self.setLayout(layout_form)

    def submit(self):
        self.complete()
        self.hide()

    def cancel(self):
        self.hide()

    def complete(self):
        print("Settings updated")
        Component.root.settings.site = self.input_location.text()
        Component.root.settings.address = self.input_address.text()
        Component.root.window.home.sidepanel.header.lbl_location.setText(Component.root.settings.site)

class LoginPopup(Popup):
    def __init__(self, ascendent):
        super(LoginPopup, self).__init__(ascendent=ascendent)
        top_margin = Style.unit * 1.5
        left_margin = Style.unit * 2.5
        main_height = int(3 * Style.unit)
        main_width = int(5 * Style.unit)
        popup_width = int(Style.unit * 2)

        self.setGeometry(left_margin + (main_width) - (popup_width / 1.8), top_margin + (main_height / 2) - (popup_width / 2), popup_width, (popup_width / 2))
        if os.name == 'nt':
            self.setWindowFlags(Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint))
        
        self.btn_submit = QPushButton('Login')
        self.btn_cancel = QPushButton('Cancel')

        self.btn_submit.setFixedWidth(int(Style.unit / 3))
        self.btn_cancel.setFixedWidth(int(Style.unit / 3))
        self.btn_cancel.setFixedHeight(int(Style.unit / 4))
        self.btn_submit.clicked.connect(self.submit)
        self.btn_cancel.clicked.connect(self.cancel)

        hbox_click = QHBoxLayout()
        hbox_click.addWidget(self.btn_submit)
        hbox_click.addWidget(self.btn_cancel)

        self.lbl_user = QLabel('Username')
        self.lbl_pass = QLabel('Password')
        self.lbl_empty = QLabel()

        self.lbl_user.setStyleSheet(Style.replace_variables('border: @None;'))
        self.lbl_pass.setStyleSheet(Style.replace_variables('border: @None;'))
        self.lbl_empty.setStyleSheet(Style.replace_variables('border: @None;'))

        self.input_username = QLineEdit('')
        self.input_password = QLineEdit('')

        self.layout = QFormLayout()
        self.layout.setAlignment(Qt.AlignRight)
        self.layout.addRow(self.lbl_user, self.input_username)
        self.layout.addRow(self.lbl_pass, self.input_password)
        self.layout.addRow(self.lbl_empty, hbox_click)

        layout_center = QVBoxLayout()
        layout_center.setAlignment(Qt.AlignTop)
        layout_center.addLayout(self.layout)

        contain_form = QWidget()
        contain_form.setLayout(layout_center)
        contain_form.setStyleSheet(Style.replace_variables('margin: @MediumMargin; \
                                                            padding: @LargePadding; \
                                                            border: @BorderThin solid @LightTextColor; \
                                                            border-radius: @SmallRadius; \
                                                            background-color: @LightColor; \
                                                            color: @LightTextColor; \
                                                            font: @ButtonTextSize @TextFont; \
                                                            font-weight: 30;'))
        layout_form = QHBoxLayout()
        layout_form.addStretch()
        layout_form.addWidget(contain_form)
        layout_form.addStretch()

        self.setLayout(layout_form)

    def submit(self):
        self.complete()
        self.hide()

    def cancel(self):
        self.hide()

    def complete(self):
        Component.root.user_login(
            self.input_username.text(),
            self.input_password.text(),
        )

class CameraPopup(Popup):
    def __init__(self, ascendent):
        super(CameraPopup, self).__init__(ascendent=ascendent)

        vbox = QVBoxLayout()
        vbox.addWidget(QLineEdit())
        vbox.addWidget(QLineEdit())

        hbox = QHBoxLayout()
        hbox.addWidget(QRadioButton('Broadcast'))
        hbox.addWidget(QRadioButton('Network'))
        hbox.addWidget(QRadioButton('Off'))
        hbox.addStretch()

        self.btn_submit = QPushButton('Submit')
        self.btn_cancel = QPushButton('Cancel')

        self.btn_submit.setFixedWidth(int(Style.unit / 3))
        self.btn_cancel.setFixedWidth(int(Style.unit / 3))
        self.btn_submit.clicked.connect(self.submit)
        self.btn_cancel.clicked.connect(self.cancel)

        hbox_click = QHBoxLayout()
        hbox_click.addWidget(self.btn_submit)
        hbox_click.addWidget(self.btn_cancel)
        hbox_click.addStretch()

        self.lbl_name = QLabel('Camera')
        self.lbl_address = QLabel('IP Address')
        self.lbl_port = QLabel('Port')
        self.lbl_protocol = QLabel('Protocol')
        self.lbl_path = QLabel('Path (Optional)')
        self.lbl_empty = QLabel()

        self.lbl_name.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_address.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_port.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_protocol.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_path.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_empty.setStyleSheet(Style.replace_variables('border: @None'))

        self.input_location = QLineEdit('Android Camera')
        # self.input_address = QLineEdit('data/sample/surveillance1.mp4')
        self.input_address = QLineEdit('10.0.0.101')
        self.input_port = QLineEdit('8080')
        self.input_protocol = QLineEdit('rtsp')
        self.input_path = QLineEdit('h264_ulaw.sdp')

        self.layout = QFormLayout()
        self.layout.setAlignment(Qt.AlignRight)
        self.layout.addRow(self.lbl_name, self.input_location)
        self.layout.addRow(self.lbl_address, self.input_address)
        self.layout.addRow(self.lbl_port, self.input_port)
        self.layout.addRow(self.lbl_protocol, self.input_protocol)
        self.layout.addRow(self.lbl_path, self.input_path)
        self.layout.addRow(self.lbl_empty, hbox_click)

        layout_center = QVBoxLayout()
        layout_center.setAlignment(Qt.AlignCenter)
        layout_center.addLayout(self.layout)

        contain_form = QWidget()
        contain_form.setLayout(layout_center)
        contain_form.setMinimumHeight(int(Style.unit * 2))
        contain_form.setStyleSheet(Style.replace_variables('margin: @MediumMargin; \
                                    padding: @LargePadding; \
                                    border: @BorderThick solid @LightTextColor; \
                                    border-radius: @SmallRadius; \
                                    background-color: @LightColor; \
                                    color: @LightTextColor; \
                                    font: @ButtonTextSize @TextFont; \
                                    font-weight: 30;'))
        layout_form = QHBoxLayout()
        layout_form.addStretch()
        layout_form.addWidget(contain_form)
        layout_form.addStretch()

        self.setLayout(layout_form)

    def submit(self):
        self.complete()
        self.hide()

    def cancel(self):
        self.hide()

    def complete(self):
        Component.root.add_camera(
            self.input_address.text(),
            self.input_port.text(),
            self.input_path.text(),
            self.input_protocol.text()
        )


class LocationPopup(Popup):
    def __init__(self, ascendent):
        super(LocationPopup, self).__init__(ascendent=ascendent)

        self.btn_submit = QPushButton('Submit')
        self.btn_cancel = QPushButton('Cancel')

        self.btn_submit.setFixedWidth(int(Style.unit / 3))
        self.btn_cancel.setFixedWidth(int(Style.unit / 3))
        self.btn_submit.clicked.connect(self.submit)
        self.btn_cancel.clicked.connect(self.cancel)

        hbox = QHBoxLayout()
        hbox.addWidget(QRadioButton('Broadcast'))
        hbox.addWidget(QRadioButton('Network'))
        hbox.addWidget(QRadioButton('Off'))
        hbox.addStretch()

        hbox_click = QHBoxLayout()
        hbox_click.addWidget(self.btn_submit)
        hbox_click.addWidget(self.btn_cancel)
        hbox_click.addStretch()

        self.lbl_id = QLabel('Location ID')
        self.lbl_location = QLabel('Location Name')
        self.lbl_address = QLabel('Priority Level (5)')
        self.lbl_streaming = QLabel('Streaming')
        self.lbl_empty = QLabel()

        self.lbl_id.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_location.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_address.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_streaming.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_empty.setStyleSheet(Style.replace_variables('border: @None'))

        self.input_id = QLabel(str(len(Component.root.get_locations())))
        self.input_id.setStyleSheet(Style.replace_variables('border: @None'))
        self.input_location = QLineEdit('Room')
        self.input_priority = QLineEdit('5')

        self.layout = QFormLayout()
        self.layout.setAlignment(Qt.AlignRight)
        self.layout.addRow(self.lbl_id, self.input_id)
        self.layout.addRow(self.lbl_location, self.input_location)
        self.layout.addRow(self.lbl_address, self.input_priority)
        self.layout.addRow(self.lbl_streaming, hbox)
        self.layout.addRow(self.lbl_empty, hbox_click)

        layout_center = QVBoxLayout()
        layout_center.setAlignment(Qt.AlignCenter)
        layout_center.addLayout(self.layout)
        
        contain_form = QWidget()
        contain_form.setLayout(layout_center)
        contain_form.setMinimumHeight(int(Style.unit * 2))
        contain_form.setStyleSheet(Style.replace_variables('margin: @MediumMargin; \
                                    padding: @LargePadding; \
                                    border: @BorderThick solid @LightTextColor; \
                                    border-radius: @SmallRadius; \
                                    background-color: @LightColor; \
                                    color: @LightTextColor; \
                                    font: @ButtonTextSize @TextFont; \
                                    font-weight: 30;'))
        layout_form = QHBoxLayout()
        layout_form.addStretch()
        layout_form.addWidget(contain_form)
        layout_form.addStretch()

        self.setLayout(layout_form)

    def submit(self):
        self.complete()
        self.hide()

    def cancel(self):
        self.hide()

    def complete(self):
        Component.root.add_location(
            self.input_location.text()
        )

