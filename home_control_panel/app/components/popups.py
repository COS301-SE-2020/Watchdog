from PyQt5.QtCore import (
    Qt,
    QSize
)
from PyQt5.QtGui import (
    QIcon,
    QPixmap
)
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QLineEdit,
    QFormLayout,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QRadioButton,
    QGraphicsDropShadowEffect
)
from .component import Component
from .style import Style


class Popup(QWidget, Component):
    def __init__(self, ascendent):
        super(Popup, self).__init__(ascendent=ascendent)
        self.setWindowFlags(Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint))
        self.setStyleSheet(Style.replace_variables(Style.light))
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet(Style.replace_variables('margin: @MediumMargin; \
                                                    padding: @SmallPadding; \
                                                    border: 1px solid @AltLightColor; \
                                                    border-radius: @SmallRadius; \
                                                    background-color: @LightColor; \
                                                    color: @LightTextColor; \
                                                    font: @ButtonTextSize @TextFont; \
                                                    font-weight: 30;'))
        self.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=12, xOffset=3, yOffset=10))

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

    def submit(self):
        self.hide()

    def cancel(self):
        self.hide()


class SettingsPopup(Popup):
    def __init__(self, ascendent):
        super(SettingsPopup, self).__init__(ascendent=ascendent)
        self.btn_submit = QPushButton('Save')
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

        self.input_location = QLineEdit(Component.root.settings.settings['site'])
        self.input_address = QLineEdit(Component.root.settings.settings['address'])

        self.layout = QFormLayout()
        self.layout.setAlignment(Qt.AlignRight)
        self.layout.addRow(self.lbl_location, self.input_location)
        self.layout.addRow(self.lbl_address, self.input_address)

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

        layout_center = QVBoxLayout()
        layout_center.setAlignment(Qt.AlignCenter)
        layout_center.addLayout(self.quit_button_container)
        layout_center.addLayout(logo_layout)
        layout_center.addLayout(self.layout)
        layout_center.addLayout(btn_layout)

        contain_form = QWidget()
        contain_form.setLayout(layout_center)
        contain_form.setStyleSheet(Style.replace_variables('margin: @MediumMargin; \
                                                            padding: @LargePadding; \
                                                            border: @BorderThin solid @AltLightColor; \
                                                            border-radius: @SmallRadius; \
                                                            background-color: @LightColor; \
                                                            color: @LightTextColor; \
                                                            font: @ButtonTextSize @TextFont; \
                                                            font-weight: 30;'))

        self.lbl_location.setStyleSheet(Style.replace_variables('border: @None;'))
        self.lbl_address.setStyleSheet(Style.replace_variables('border: @None;'))
        self.lbl_streaming.setStyleSheet(Style.replace_variables('border: @None;'))
        self.lbl_empty.setStyleSheet(Style.replace_variables('border: @None;'))
        self.icon_home.setStyleSheet(Style.replace_variables('border: @None;'))

        layout_form = QHBoxLayout()
        layout_form.addStretch()
        layout_form.addWidget(contain_form)
        layout_form.addStretch()

        self.setLayout(layout_form)
        self.quit_button.show()

    def submit(self):
        self.complete()
        self.hide()

    def cancel(self):
        self.hide()

    def complete(self):
        print("Settings updated")
        Component.root.settings.change_setting('site', value=self.input_location.text())
        Component.root.settings.change_setting('address', value=self.input_address.text())
        Component.root.window.home.sidepanel.header.lbl_location.setText(Component.root.settings.settings['site'])


class LocationPopup(Popup):
    def __init__(self, ascendent):
        super(LocationPopup, self).__init__(ascendent=ascendent)

        self.btn_submit = QPushButton('Save')
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
        self.input_priority = QLineEdit('5')

        self.layout = QFormLayout()
        self.layout.setAlignment(Qt.AlignRight)
        self.layout.addRow(self.lbl_id, self.input_id)
        self.layout.addRow(self.lbl_location, self.input_location)
        self.layout.addRow(self.lbl_address, self.input_priority)
        
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.addWidget(self.btn_submit)
        btn_layout.setContentsMargins(0, 0, 0, Style.unit / 4)

        layout_center = QVBoxLayout()
        layout_center.setAlignment(Qt.AlignCenter)
        layout_center.addLayout(self.quit_button_container)
        layout_center.addLayout(self.layout)
        layout_center.addLayout(btn_layout)

        contain_form = QWidget()
        contain_form.setLayout(layout_center)
        contain_form.setStyleSheet(Style.replace_variables('margin: @MediumMargin; \
                                    padding: @LargePadding; \
                                    border: @BorderThick solid @AltLightColor; \
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
        self.quit_button.show()

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

        vbox = QVBoxLayout()
        vbox.addWidget(QLineEdit())
        vbox.addWidget(QLineEdit())

        hbox = QHBoxLayout()
        hbox.addWidget(QRadioButton('Intuder Alarm'))
        hbox.addWidget(QRadioButton('Home Surveillance'))
        hbox.addWidget(QRadioButton('Offline'))
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

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.addWidget(self.btn_submit)
        btn_layout.setContentsMargins(0, 0, 0, Style.unit / 4)

        layout_center = QVBoxLayout()
        layout_center.setAlignment(Qt.AlignCenter)
        layout_center.addLayout(self.quit_button_container)
        layout_center.addLayout(self.layout)
        layout_center.addLayout(btn_layout)

        contain_form = QWidget()
        contain_form.setLayout(layout_center)
        contain_form.setMinimumHeight(int(Style.unit * 2))
        contain_form.setStyleSheet(Style.replace_variables('margin: @MediumMargin; \
                                    padding: @LargePadding; \
                                    border: @BorderThick solid @AltLightColor; \
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
        self.quit_button.show()

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


class LoginPopup(Popup):
    def __init__(self, ascendent):
        super(LoginPopup, self).__init__(ascendent=ascendent)
        self.logged_in = False

        popup_width = Style.width
        popup_height = Style.height / 2
        self.setGeometry((Style.screen_width / 2) - (popup_width / 2), (Style.screen_height / 2) - (popup_height / 2), popup_width, popup_height)

        self.btn_submit = QPushButton('Login')
        self.btn_submit.setFixedWidth(int(Style.unit / 3))
        self.btn_submit.clicked.connect(self.submit)

        hbox_click = QHBoxLayout()
        hbox_click.addWidget(self.btn_submit)

        self.lbl_user = QLabel('Username')
        self.lbl_pass = QLabel('Password')
        self.lbl_empty = QLabel()

        self.input_username = QLineEdit('')
        self.input_password = QLineEdit('')
        self.input_password.setEchoMode(QLineEdit.Password)

        self.input_username.setFixedWidth(self.width * 0.15)
        self.input_password.setFixedWidth(self.width * 0.15)

        self.input_username.returnPressed.connect(self.submit)
        self.input_password.returnPressed.connect(self.submit)
        
        self.layout = QFormLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addRow(self.lbl_user, self.input_username)
        self.layout.addRow(self.lbl_pass, self.input_password)

        map_logo = QPixmap('assets/icons/watchdog.png')
        self.icon_logo = QLabel()
        self.icon_logo.setPixmap(map_logo.scaled(Style.sizes.icon_logo * 1.2, Style.sizes.icon_logo * 1.2, Qt.KeepAspectRatio, Qt.FastTransformation))
        self.lbl_message = QLabel('Please log in to your Watchdog Account.')
        self.lbl_warning = QLabel('Invalid login details.')
        self.lbl_warning.hide()

        logo_layout = QHBoxLayout()
        logo_layout.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(self.icon_logo)

        message_layout = QHBoxLayout()
        message_layout.setAlignment(Qt.AlignCenter)
        message_layout.addWidget(self.lbl_message)

        warning_layout = QHBoxLayout()
        warning_layout.setContentsMargins(0, 0, 0, 0)
        warning_layout.setAlignment(Qt.AlignCenter)
        warning_layout.addWidget(self.lbl_warning)

        form_layout = QHBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)
        form_layout.addStretch()
        form_layout.addLayout(self.layout)
        form_layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.addWidget(self.btn_submit)
        btn_layout.setContentsMargins(0, 0, 0, Style.unit / 4)

        layout_center = QVBoxLayout()
        layout_center.setAlignment(Qt.AlignCenter)
        layout_center.addLayout(self.quit_button_container)
        layout_center.addLayout(logo_layout)
        layout_center.addLayout(message_layout)
        layout_center.addLayout(warning_layout)
        layout_center.addLayout(form_layout)
        layout_center.addLayout(btn_layout)

        contain_form = QWidget()
        contain_form.setLayout(layout_center)
        contain_form.setStyleSheet(Style.replace_variables('margin: @MediumMargin; \
                                                            padding: @LargePadding; \
                                                            border: 1px solid @AltLightColor; \
                                                            border-radius: @SmallRadius; \
                                                            background-color: @LightColor; \
                                                            color: @LightTextColor; \
                                                            font: @ButtonTextSize @TextFont; \
                                                            font-weight: 30;'))

        self.lbl_user.setStyleSheet(Style.replace_variables('border: @None;'))
        self.lbl_pass.setStyleSheet(Style.replace_variables('border: @None;'))
        self.lbl_empty.setStyleSheet(Style.replace_variables('border: @None;'))
        self.icon_logo.setStyleSheet(Style.replace_variables('border: @None;'))
        self.lbl_message.setStyleSheet(Style.replace_variables('border: @None; font: @SmallTextSize @TextFont;'))
        self.lbl_warning.setStyleSheet(Style.replace_variables('border: @None; font: @SmallTextSize @TextFont; color: red;'))

        layout_form = QHBoxLayout()
        layout_form.addStretch()
        layout_form.addWidget(contain_form)
        layout_form.addStretch()

        self.setLayout(layout_form)

    def submit(self):
        self.complete()

    def complete(self):
        res = Component.root.user_login(
            self.input_username.text(),
            self.input_password.text()
        )
        if res:
            self.lbl_warning.hide()
            self.quit_button.show()
            self.hide()
            Component.root.window.home.view.header.btn_user.show()
        else:
            self.lbl_warning.show()
            Component.root.window.home.view.header.btn_user.show()