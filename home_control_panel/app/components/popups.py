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


class Popup(QWidget, Component):
    def __init__(self, ascendent):
        super(Popup, self).__init__(ascendent=ascendent)
        # if os.name == 'nt':
        #     self.setWindowFlags(Qt.WindowFlags(Qt.FramelessWindowHint))
        self.setWindowFlags(Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint))
        self.setStyleSheet(Style.replace_variables(Style.light))
        self.setAttribute(Qt.WA_TranslucentBackground, True)
<<<<<<< Updated upstream
        self.setStyleSheet(Style.replace_variables('padding: @LargePadding;'))
=======
        self.setStyleSheet(Style.replace_variables('margin: @MediumMargin; \
                                                    padding: @SmallPadding; \
                                                    border: 1px solid @AltLightColor; \
                                                    border-radius: @SmallRadius; \
                                                    background-color: @LightColor; \
                                                    color: @LightTextColor; \
                                                    font: @ButtonTextSize @TextFont; \
                                                    font-weight: 30;'))
        self.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=12, xOffset=3, yOffset=3))

        self.quit_button = QPushButton()
        self.quit_button.clicked.connect(self.cancel)

        map_user = QPixmap('assets/icons/quit.png')
        self.quit_button.setIcon(QIcon(map_user))
        self.quit_button.setIconSize(QSize(25, 25))
        self.quit_button.setStyleSheet(Style.replace_variables('margin: @None; padding: @None; border: @None;'))

        self.quit_button_container = QHBoxLayout()
        self.quit_button_container.setContentsMargins(0, 0, 0, 0)
        self.quit_button_container.setAlignment(Qt.AlignRight)
        self.quit_button_container.addStretch(1)
        self.quit_button_container.addWidget(self.quit_button)

        self.quit_button.hide()
>>>>>>> Stashed changes

    def submit(self):
        self.hide()

    def cancel(self):
        self.hide()


class SettingsPopup(Popup):
    def __init__(self, ascendent):
        super(SettingsPopup, self).__init__(ascendent=ascendent)
<<<<<<< Updated upstream
=======
        popup_width = Style.width
        popup_height = Style.height
        self.setGeometry(Style.h_margin + ((Style.width - popup_width) / 2), Style.v_margin + ((Style.height - popup_height) / 2), popup_width, popup_height)
>>>>>>> Stashed changes

        hbox = QHBoxLayout()
        hbox.addWidget(QRadioButton('Broadcast'))
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

        self.input_location = QLineEdit(Component.root.settings.settings['site'])
        self.input_address = QLineEdit(Component.root.settings.settings['address'])

        self.layout = QFormLayout()
        self.layout.setAlignment(Qt.AlignRight)
        self.layout.addRow(self.lbl_location, self.input_location)
        self.layout.addRow(self.lbl_address, self.input_address)
<<<<<<< Updated upstream
        self.layout.addRow(self.lbl_empty, hbox_click)

        layout_center = QVBoxLayout()
        layout_center.setAlignment(Qt.AlignCenter)
=======
        self.layout.addRow(widget_clips, self.input_clips)

        map_home = QPixmap('assets/icons/home.png')
        self.icon_home = QLabel()
        self.icon_home.setPixmap(map_home.scaled(Style.sizes.icon_medium, Style.sizes.icon_medium, Qt.KeepAspectRatio, Qt.FastTransformation))

        logo_layout = QHBoxLayout()
        logo_layout.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(self.icon_home)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.addWidget(self.btn_submit)
        btn_layout.setContentsMargins(0, 0, 0, Style.unit / 4)
        
        map_user = QPixmap('assets/icons/user.png')
        self.btn_user = QPushButton()
        self.btn_user.clicked.connect(self.toggle_login)
        self.btn_user.setIcon(QIcon(map_user))
        self.btn_user.setIconSize(QSize(25, 25))
        
        user_container = QHBoxLayout()
        user_container.setContentsMargins(0, 0, 0, 0)
        user_container.setAlignment(Qt.AlignCenter)
        user_container.addStretch()
        user_container.addWidget(self.btn_user)
        user_container.addStretch()

        layout_center = QVBoxLayout()
        layout_center.setAlignment(Qt.AlignCenter)
        layout_center.addLayout(self.quit_button_container)
        layout_center.addLayout(logo_layout)
        layout_center.addLayout(user_container)
>>>>>>> Stashed changes
        layout_center.addLayout(self.layout)

        contain_form = QWidget()
        contain_form.setLayout(layout_center)
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

    def toggle_login(self):
        Component.root.login_screen.show()

    def submit(self):
        self.complete()
        self.hide()

    def cancel(self):
        self.hide()

    def complete(self):
        print("Settings updated")
        name = self.input_location.text()[:20]
        Component.root.settings.change_setting('site', value=name)
        Component.root.settings.change_setting('address', value=self.input_address.text())
        Component.root.window.home.sidepanel.header.lbl_location.setText(Component.root.settings.settings['site'])


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
        hbox.addWidget(QRadioButton('Live'))
        hbox.addWidget(QRadioButton('Offline'))
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
        # self.input_priority = QLineEdit('5')

        self.layout = QFormLayout()
        self.layout.setAlignment(Qt.AlignRight)
        self.layout.addRow(self.lbl_id, self.input_id)
        self.layout.addRow(self.lbl_location, self.input_location)
<<<<<<< Updated upstream
        self.layout.addRow(self.lbl_address, self.input_priority)
        self.layout.addRow(self.lbl_empty, hbox_click)
=======
        # self.layout.addRow(self.lbl_address, self.input_priority)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.addWidget(self.btn_submit)
        btn_layout.setContentsMargins(0, 0, 0, Style.unit / 4)
>>>>>>> Stashed changes

        layout_center = QVBoxLayout()
        layout_center.setAlignment(Qt.AlignCenter)
        layout_center.addLayout(self.layout)

        contain_form = QWidget()
        contain_form.setLayout(layout_center)
<<<<<<< Updated upstream
        contain_form.setStyleSheet(Style.replace_variables('margin: @MediumMargin; \
                                    padding: @LargePadding; \
                                    border: @BorderThick solid @LightTextColor; \
                                    border-radius: @SmallRadius; \
                                    background-color: @LightColor; \
                                    color: @LightTextColor; \
                                    font: @ButtonTextSize @TextFont; \
                                    font-weight: 30;'))
=======
        contain_form.setStyleSheet(Style.replace_variables('margin: @SmallMargin; \
                                                            padding: @LargePadding; \
                                                            border: @BorderThick solid @AltLightColor; \
                                                            border-radius: @SmallRadius; \
                                                            background-color: @LightColor; \
                                                            color: @LightTextColor; \
                                                            font: @ButtonTextSize @TextFont; \
                                                            font-weight: 30;'))
>>>>>>> Stashed changes
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


class CameraPopup(Popup):
    def __init__(self, ascendent, label='', address='', port='', protocol='', path=''):
        super(CameraPopup, self).__init__(ascendent=ascendent)
<<<<<<< Updated upstream

        vbox = QVBoxLayout()
        vbox.addWidget(QLineEdit())
        vbox.addWidget(QLineEdit())

        hbox = QHBoxLayout()
        hbox.addWidget(QRadioButton('Intuder Alarm'))
        hbox.addWidget(QRadioButton('Home Surveillance'))
        hbox.addWidget(QRadioButton('Offline'))
        hbox.addStretch()
=======
        popup_width = Style.width
        popup_height = Style.height
        self.setGeometry(Style.h_margin + ((Style.width - popup_width) / 2), Style.v_margin + ((Style.height - popup_height) / 2), popup_width, popup_height)

        self.lbl_warning = QLabel('Could not connect to IP Camera!')
        self.lbl_warning.hide()
        warning_layout = QHBoxLayout()
        warning_layout.setContentsMargins(0, 0, 0, 0)
        warning_layout.setAlignment(Qt.AlignCenter)
        warning_layout.addWidget(self.lbl_warning)
        self.lbl_warning.setStyleSheet(Style.replace_variables('border: @None; font: @SmallTextSize @TextFont; color: red;'))
>>>>>>> Stashed changes

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

        self.lbl_location = QLabel('Room')
        self.lbl_name = QLabel('Camera')
        self.lbl_address = QLabel('IP Address')
        self.lbl_port = QLabel('Port')
        self.lbl_protocol = QLabel('Protocol')
        self.lbl_path = QLabel('Path (Optional)')
        self.lbl_empty = QLabel()

        self.lbl_location.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_name.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_address.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_port.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_protocol.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_path.setStyleSheet(Style.replace_variables('border: @None'))
        self.lbl_empty.setStyleSheet(Style.replace_variables('border: @None'))

        self.lbl_current_location = QLabel(Component.root.current_location)
        self.input_location = QLineEdit(label)
        self.input_address = QLineEdit(address)
        self.input_port = QLineEdit(port)
        self.input_protocol = QLineEdit(protocol)
        self.input_path = QLineEdit(path)

        self.layout = QFormLayout()
        self.layout.setAlignment(Qt.AlignRight)
        self.layout.addRow(self.lbl_location, self.lbl_current_location)
        self.layout.addRow(self.lbl_name, self.input_location)
        self.layout.addRow(self.lbl_address, self.input_address)
        self.layout.addRow(self.lbl_port, self.input_port)
        self.layout.addRow(self.lbl_protocol, self.input_protocol)
        self.layout.addRow(self.lbl_path, self.input_path)
<<<<<<< Updated upstream
        self.layout.addRow(self.lbl_empty, hbox_click)
=======

        self.btn_webcam = QPushButton()
        self.btn_webcam.clicked.connect(self.complete_webcam)
        map_cam = QPixmap('assets/icons/webcam.png')
        self.btn_webcam.setIcon(QIcon(map_cam))
        self.btn_webcam.setIconSize(QSize(Style.sizes.icon_small, Style.sizes.icon_small))

        webcam_layout = QHBoxLayout()
        webcam_layout.setAlignment(Qt.AlignCenter)
        webcam_layout.addWidget(self.btn_webcam)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.addWidget(self.btn_submit)
        # btn_layout.setContentsMargins(0, 0, 0, Style.unit / 4)
>>>>>>> Stashed changes

        layout_center = QVBoxLayout()
        layout_center.setAlignment(Qt.AlignCenter)
        layout_center.addLayout(self.layout)

        contain_form = QWidget()
        contain_form.setLayout(layout_center)
        contain_form.setMinimumHeight(int(Style.unit * 2))
<<<<<<< Updated upstream
        contain_form.setStyleSheet(Style.replace_variables('margin: @MediumMargin; \
                                    padding: @LargePadding; \
                                    border: @BorderThick solid @LightTextColor; \
                                    border-radius: @SmallRadius; \
                                    background-color: @LightColor; \
                                    color: @LightTextColor; \
                                    font: @ButtonTextSize @TextFont; \
                                    font-weight: 30;'))
=======
        contain_form.setStyleSheet(Style.replace_variables('margin: @SmallMargin; \
                                                            padding: @LargePadding; \
                                                            border: @BorderThick solid @AltLightColor; \
                                                            border-radius: @SmallRadius; \
                                                            background-color: @LightColor; \
                                                            color: @LightTextColor; \
                                                            font: @ButtonTextSize @TextFont; \
                                                            font-weight: 30;'))
>>>>>>> Stashed changes
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
            self.lbl_current_location.text(),
            self.input_address.text(),
            self.input_port.text(),
            self.input_path.text(),
            self.input_protocol.text()
        )

<<<<<<< Updated upstream
=======
    def complete_webcam(self):
        Component.root.add_camera(
            self.lbl_current_location.text(),
            'Webcam',
            '0',
            '',
            '',
            ''
        )
        self.lbl_warning.hide()
        self.hide()

>>>>>>> Stashed changes

class LoginPopup(Popup):
    def __init__(self, ascendent):
        super(LoginPopup, self).__init__(ascendent=ascendent)

<<<<<<< Updated upstream
        popup_width = Style.width / 5
        popup_height = Style.height / 5
        self.setGeometry(Style.h_margin + (Style.width - popup_width), Style.v_margin + popup_height, popup_width, popup_height)
=======
        popup_width = Style.width * 1.5
        popup_height = Style.height
        self.setGeometry(Style.h_margin + ((Style.width - popup_width) / 2), Style.v_margin + ((Style.height - popup_height) / 2), popup_width, popup_height)
>>>>>>> Stashed changes

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
        self.input_password.setEchoMode(QLineEdit.Password)

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
        contain_form.setStyleSheet(Style.replace_variables('margin: @SmallMargin; \
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

<<<<<<< Updated upstream

class LoginContainer(QWidget, Component):
    def __init__(self, ascendent=None):
        super(LoginContainer, self).__init__(ascendent=ascendent)

        self.setFixedWidth(Style.unit * 0.75)
        self.setFixedHeight(ascendent.height)

        self.lbl_user = QLabel('Username')
        self.lbl_pass = QLabel('Password')

        self.input_username = QLineEdit('')
        self.input_password = QLineEdit('')

        self.layout = QFormLayout()
        self.layout.setAlignment(Qt.AlignRight)

        self.layout.addRow(self.lbl_user, self.input_username)
        self.layout.addRow(self.lbl_pass, self.input_password)

        self.input_password.setEchoMode(QLineEdit.Password)

        layout_center = QHBoxLayout()
        layout_center.setAlignment(Qt.AlignCenter)
        layout_center.addLayout(self.layout)

        contain_form = QWidget()
        contain_form.setLayout(layout_center)
        contain_form.setStyleSheet(Style.replace_variables('margin: 0px;  \
                                                            padding: @LargePadding; \
                                                            background-color: transparent; \
                                                            color: @LightTextColor; \
                                                            font: @ButtonTextSize @TextFont; \
                                                            border-radius: @SmallRadius; \
                                                            font-weight: 30;'))

        self.lbl_user.setStyleSheet(Style.replace_variables('border: @None;'))
        self.lbl_pass.setStyleSheet(Style.replace_variables('border: @None;'))

        self.input_username.setStyleSheet(Style.replace_variables('border: @BorderThin solid @LightTextColor;'))
        self.input_password.setStyleSheet(Style.replace_variables('border: @BorderThin solid @LightTextColor;'))

        self.input_username.returnPressed.connect(self.submit)
        self.input_password.returnPressed.connect(self.submit)

        layout_form = QVBoxLayout()
        layout_form.setAlignment(Qt.AlignCenter)
        layout_form.addWidget(contain_form)

        self.setLayout(layout_form)

        self.hide()

    def submit(self):
        if self.input_username.text() != '':
            self.complete()
        self.hide()

    def cancel(self):
        self.hide()

    def complete(self):
        Component.root.user_login(
            self.input_username.text(),
            self.input_password.text(),
        )
=======
        if res:
            self.lbl_warning.hide()
            self.quit_button.show()
            self.hide()
            # Component.root.window.home.view.header.btn_user.show()
            Component.root.setup()
        else:
            self.lbl_warning.show()
>>>>>>> Stashed changes
